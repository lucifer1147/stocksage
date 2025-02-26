import os
import json
import logging

import torch
import torch.nn as nn
import torch.optim as optim

from .utils import prepareInput, plotLossGraph, checkZeroGrad
from .neuralnet import getDevice, StockDataset, Model, init_weights

rootDir = os.path.dirname(__file__)

def train(
        tickers: list[str],
        saveExtrasToFile: bool = False,
        trainingPeriod: str = 'max',
        timeFrame: int = 20, 
        features: list[str] = ['Open', 'High', 'Low', 'Close', 'Volume', 'Day', 'Date', 'Month', 'Year'], 
        addFeatures: list[str] = [],
        
        hiddenSize: int = 512,
        numLayers: int = 5,
        batchSize: int = 16,
        learningRate: float = 0.001, 
        dropoutProb: float = 0.2,
        outputSize: int = 5,
        
        saveModelAs: str = None,
        fromExisting: str = None,
        checkpointsIter: int = None,
        fromCheckpoint: str = None,
        
        verbose: bool = True,
        debug: bool = False,
        sanityCheck: bool = False,
        logToFile: bool = True,
        
        maxEpochs: int = 50,
        minEpochs: int = 5,
        forceCompleteEpochs: bool = False,
        
        optimizerChoice: str = 'adamw',
        schedulerChoice: str = 'cosineannealinglr',
        patience: int = 10,
        
        plotLoss: bool = True,
        callback: callable = None
    ):
    
    DEVICE = getDevice()
    inputSize = len(features) + len(addFeatures)
    
    if saveModelAs is not None or saveExtrasToFile is not None:
        os.makedirs(os.path.join(rootDir, f'./Models/{saveModelAs}_files/'), exist_ok=True)
        
        if checkpointsIter is not None:
            os.makedirs(os.path.join(rootDir, f'./Models/{saveModelAs}_files/Checkpoints/'), exist_ok=True)
        
    if logToFile:
        logger = logging.getLogger(__name__)
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        
        formatter = '%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s    [%(relativeCreated)d]'
        logging.basicConfig(
            filename=os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}_training.log'),
            format=formatter,
            filemode='w'
        )
    
    trainConfig = {
        "tickers": tickers,
        "timeFrame": timeFrame,
        "features": features,
        "addFeatures": addFeatures,
        
        "hiddenSize": hiddenSize,
        "numLayers": numLayers,
        "inputSize": inputSize,
        "outputSize": outputSize,
        "dropoutProb": dropoutProb,
        
        "learningRate": learningRate,
        "batchSize": batchSize,
        
        "saveModelAs": saveModelAs,
        "saveExtrasToFile": saveExtrasToFile,
        
        "checkpointsIter": checkpointsIter,
        "optimizerChoice": optimizerChoice,
        "schedulerChoice": schedulerChoice,
        
        "maxEpochs": maxEpochs,
        "patience": patience,
        "minEpochs": minEpochs,
    }
    
    if logToFile:
        logger.info('Training Config:\n\t' + json.dumps(trainConfig, indent=4))
        
    if callback:
        callback({
            'message': f"Training Config:\n\t{json.dumps(trainConfig, indent=4)}"
        })
    
    if saveModelAs is not None:
        with open(os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}_train_config.json'), 'w') as f:
            json.dump(trainConfig, f, indent=4)
    
    if verbose:
        print(f"Starting Training [Using: {DEVICE}]...")
    if logToFile:
        logger.info(f"Starting Training [Using: {DEVICE}]...")
        if DEVICE == 'cpu':
            logger.warning('Training on CPU!')
    if callback:
        msg = {
            'message': f"Starting Training [Using: {DEVICE}]...",
        }
        if DEVICE == 'cpu':
            msg['warning'] = 'Training on CPU!'
        
        callback(msg)
        
    
    saveToFile = None
    if saveExtrasToFile:
        saveToFile = saveModelAs
        
    X, y = prepareInput(tickers, saveToFile=saveToFile, timeframe=timeFrame, features=features, period=trainingPeriod, addFeatures=addFeatures, logToFile=logToFile)

    if verbose:
        print("\nInputs and targets Loaded:")

        print('\tX Shape:', X.shape)
        print('\tY Shape:', y.shape)
        
    if callback:
        callback({
            'message': 'Inputs and targets Loaded:\n\tX Shape: ' + str(X.shape) + '\n\tY Shape: ' + str(y.shape),
        })

    if logToFile:
        logger.info(f"Input and target sizes: X: {X.shape}, y: {y.shape}")
        
        if len(X) != len(y):
            logger.error(f"Input and target sizes do not match! X: {len(X)}, y: {len(y)}")
        if X.shape[1] != timeFrame:
            logger.error(f"Timeframe does not match! X: {X.shape[1]}, timeFrame: {timeFrame}")
        if X.shape[2] != inputSize:
            logger.error(f"Input size does not match! X: {X.shape[2]}, inputSize: {inputSize}")
        if y.shape[1] != outputSize:
            logger.error(f"Output size does not match! y: {y.shape[1]}, outputSize: {outputSize}")

    if len(X) != len(y):
        raise ValueError(f"Input and target sizes do not match! X: {len(X)}, y: {len(y)}")

    dataset = StockDataset(X, y)

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batchSize, shuffle=True, pin_memory=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batchSize, shuffle=False, pin_memory=True)
    
    if logToFile:
        logger.info(f"Dataset sizes: train: {len(train_dataset)}, val: {len(val_dataset)}")
    if callback:
        callback({
            'message': f"Dataset sizes: train: {len(train_dataset)}, val: {len(val_dataset)}",
        })

    model = Model(inputSize, hiddenSize, numLayers, outputSize, dropoutProb).to(DEVICE)
    model.apply(init_weights)
    
    if fromExisting is not None:
        if logToFile:
            logger.info(f"Loading existing model: {os.path.join(rootDir, f'./{fromExisting}_files/{fromExisting}.pth')}")
        if callback:
            callback({
                'message': f"Loading existing model: {os.path.join(rootDir, f'./{fromExisting}_files/{fromExisting}.pth')}",
            })
        model.load_state_dict(torch.load(os.path.join(rootDir, f'./{fromExisting}_files/{fromExisting}.pth')))
    
    model = model.to(DEVICE)
    
    if sanityCheck:
        for inputs, targets in train_dataset:
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            if verbose:
                print(f'\nSanity Check: Model Device: {next(model.parameters()).device}')    
                print(f"Sanity Check: Inputs dtype: {inputs.dtype}, device: {inputs.device}")
                print(f'Sanity Check: Input Shape: {inputs.shape}\t Target Shape: {targets.shape}')
                print(f"Sanity Check: Targets dtype: {targets.dtype}, device: {targets.device}")  
            if logToFile:
                logger.debug(f"Sanity Check: Model Device: {next(model.parameters()).device}")
                logger.debug(f"Sanity Check: Input Shape: {inputs.shape}\t Target Shape: {targets.shape}")
                logger.debug(f"Sanity Check: Inputs dtype: {inputs.dtype}, device: {inputs.device}")
                logger.debug(f"Sanity Check: Targets dtype: {targets.dtype}, device: {targets.device}")
            if callback:
                callback({
                    'message': f"Sanity Check: Model Device: {next(model.parameters()).device}",
                    'sanityCheck': True,
                })
                callback({
                    'message': f"Sanity Check: Inputs dtype: {inputs.dtype}, device: {inputs.device}",
                    'sanityCheck': True,
                })
                callback({
                    'message': f"Sanity Check: Input Shape: {inputs.shape}\t Target Shape: {targets.shape}",
                    'sanityCheck': True,
                })
                callback({
                    'message': f"Sanity Check: Targets dtype: {targets.dtype}, device: {targets.device}",
                    'sanityCheck': True,
                })
            break
        
    if verbose: 
        if not fromExisting:
            print("\nInitialized Model!")
        else:
            print('\nLoaded Existing Model!')
            
    if callback:
        if not fromExisting:
            callback({
                'message': 'Initialized Model!',
            })
        else:
            callback({
                'message': 'Loaded Existing Model!',
            })

    criterion = nn.MSELoss()
    
    optimizerDict = {
        'adam': optim.Adam(model.parameters(), lr=learningRate),
        'adamw': optim.AdamW(model.parameters(), lr=learningRate),
        'rmsprop': optim.RMSprop(model.parameters(), lr=learningRate)
    }
    optimizer = optimizerDict[optimizerChoice]
    
    schedulerDict = {
        'step': torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.05),
        'reduceonplateau': torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5),
        'cosineannealinglr': torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=maxEpochs)
    }
    scheduler = schedulerDict[schedulerChoice]

    if logToFile:
        logger.info(f"Optimizer: Using {optimizerChoice}")
        logger.info(f"Scheduler: Using {schedulerChoice}")
        logger.info(f"Loss Criterion: Using Mean Squared Error")      

    if callback:
        callback({
            'message': f"Optimizer: Using {optimizerChoice}\nScheduler: Using {schedulerChoice}\nLoss Criterion: Using Mean Squared Error",
        })
    if verbose:
        print("\nTraining Model:")
    if logToFile:
        logger.info("Started Training:")

    once = True

    start_epoch = 0
    if fromCheckpoint is not None:
        checkpoint = torch.load(os.path.join(rootDir, f'./{fromCheckpoint[:fromCheckpoint.find("_checkpoint_")]}_files/Checkpoints/{fromCheckpoint}.pth'))
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        start_epoch = checkpoint['epoch'] + 1

        if verbose:
            print('Loaded Checkpoint!')
        if logToFile:
            logger.info(f'Loaded Checkpoint from {os.path.join(rootDir, f'./{fromCheckpoint[:fromCheckpoint.find("_checkpoint_")]}_files/Checkpoints/{fromCheckpoint}.pth')}!')
        if callback:
            callback({
                'message': f'Loaded Checkpoint from {os.path.join(rootDir, f'./{fromCheckpoint[:fromCheckpoint.find("_checkpoint_")]}_files/Checkpoints/{fromCheckpoint}.pth')}!',
            })

    best_val_loss = float('inf')
    counter = 0
    best_model = model.state_dict()
    
    train_losses, val_losses = [], []
    
    for epoch in range(start_epoch, maxEpochs):

        model.train()
        train_loss = 0  
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()   
        train_losses.append(train_loss/len(train_dataset)) 

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
                
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                
                if debug and once:
                    print(f"Debug: Outputs shape: {outputs.shape}, Targets shape: {targets.shape}")
                    if logToFile:
                        logger.debug(f"Debug: Outputs shape: {outputs.shape}, Targets shape: {targets.shape}")
                    once = False
                    if callback:
                        callback({
                            'message': f"Debug: Outputs shape: {outputs.shape}, Targets shape: {targets.shape}",
                            'debug': True,
                        })
                
                val_loss += loss.item()
        val_losses.append(val_loss/len(val_dataset))
        
        if schedulerChoice == 'reduceonplateau':
            scheduler.step(val_loss)
        else:        
            scheduler.step()
        
        if val_loss < best_val_loss:
            if debug:
                if verbose:
                    print(f"\tBest val loss improved from {best_val_loss:.4f} to {val_loss:.4f}")
                if logToFile:
                    logger.debug(f'Best val loss improved from {best_val_loss:.4f} to {val_loss:.4f}')  
                if callback:
                    callback({
                        'message': f"Best val loss improved from {best_val_loss:.4f} to {val_loss:.4f}",
                        'debug': True,
                    })
            
            best_model = model.state_dict()
            best_val_loss = val_loss
            counter = 0 
        else:
            counter += 1
            
        if (counter >= patience) and (not forceCompleteEpochs) and (epoch > minEpochs):
            if verbose:
                print("Early stopping triggered!")
            if logToFile:
                logger.info(f"Early stopping triggered! With best loss: {best_val_loss}")
            if callback:
                callback({
                    'message': f"Early stopping triggered! With best loss: {best_val_loss}"
                })
                
            if checkpointsIter is not None:
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': best_model,
                    'optimizer_state_dict': optimizer.state_dict(),
                    'scheduler_state_dict': scheduler.state_dict(),
                }, os.path.join(rootDir, f'./Models/{saveModelAs}_files/Checkpoints/{saveModelAs}_checkpoint_{epoch}_early.pth'))
                
                if verbose:
                    print(f"\t\tCheckpoint saved as '{saveModelAs}_checkpoint_{epoch}_early.pth'")
                if logToFile:
                    logger.info(f"Checkpoint saved as {os.path.join(rootDir, f'./Models/{saveModelAs}_files/Checkpoints/{saveModelAs}_checkpoint_{epoch}_early.pth')}")
                if callback:
                    callback({
                        'message': f"Checkpoint saved as {os.path.join(rootDir, f'./Models/{saveModelAs}_files/Checkpoints/{saveModelAs}_checkpoint_{epoch}_early.pth')}"
                    })
            
            break
        
        if checkpointsIter is not None:
            if (epoch%checkpointsIter == 0 or epoch == maxEpochs-1) and epoch != 0 and saveModelAs is not None:  
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': best_model,
                    'optimizer_state_dict': optimizer.state_dict(),
                    'scheduler_state_dict': scheduler.state_dict(),
                }, os.path.join(rootDir, f'./Models/{saveModelAs}_files/Checkpoints/{saveModelAs}_checkpoint_{epoch}.pth'))
                
                if verbose:
                    print(f"\t\tCheckpoint saved as '{saveModelAs}_checkpoint_{epoch}.pth'")
                if logToFile:
                    logger.info(f"Checkpoint saved as {os.path.join(rootDir, f'./Models/{saveModelAs}_files/Checkpoints/{saveModelAs}_checkpoint_{epoch}.pth')}")
                if callback:
                    callback({
                        'message': f"Checkpoint saved as {os.path.join(rootDir, f'./Models/{saveModelAs}_files/Checkpoints/{saveModelAs}_checkpoint_{epoch}.pth')}"
                    })
            
        if verbose:
            print(f"\tEpoch [{epoch+1}/{maxEpochs}], Train Loss: {train_loss / len(train_loader):.4f}, Val Loss: {val_loss / len(val_loader):.4f}")
        if logToFile:
            logger.info(f"Epoch [{epoch+1}/{maxEpochs}], Train Loss: {train_loss / len(train_loader):.4f}, Val Loss: {val_loss / len(val_loader):.4f}")
        if callback:
            callback({
                'message': f"Epoch [{epoch+1}/{maxEpochs}], Train Loss: {train_loss / len(train_loader):.4f}, Val Loss: {val_loss / len(val_loader):.4f}"
            })


    if debug:
        print()
        checkZeroGrad(model, logToFile, callback)

    if verbose:
        print("\nTraining Complete!")
        print("\nBest validation loss achieved:", best_val_loss)
        
    if logToFile:
        logger.info("\nTraining Complete!")
        logger.info(f"Best validation loss achieved: {best_val_loss}")
        
    if callback:
        callback({
            'message': f"Training Complete!\nBest validation loss achieved: {best_val_loss}"
        })
    
    if plotLoss:
        if verbose:
            print("Plotting Loss Graphs...")
        if logToFile:
            logger.info("Plotting Loss Graphs...")
        if callback:
            callback({
                'message': "Plotting Loss Graphs..."
            })
        
        plotLossGraph(train_losses, val_losses, saveModelAs)
        
        if verbose:
            print("Loss Graph saved at:", os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}_loss_graph.png'))
        if logToFile:
            logger.info(f"Loss Graph saved at: {os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}_loss_graph.png')}")
        if callback:
            callback({
                'message': f"Loss Graph saved at: {os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}_loss_graph.png')}"
            })
    
    if saveModelAs is not None:
        print("Saving Model...")

        torch.save(best_model, os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}.pth'))
        print(f"Model saved to as '{saveModelAs}.pth' !")
        
        if logToFile:
            logger.info(f"Training Complete! Model saved to as {os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}.pth')}!")
            logger.info(f"Best validation loss achieved: {best_val_loss}")
            print('Log file saved at:', os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}_training.log'))
        if callback:
            callback({
                'message': f"Training Complete! Model saved to as {os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}.pth')}!"
            })    
            callback({
                'message': f"Best validation loss achieved: {best_val_loss}"
            })  
        
    else:    
        if logToFile:
            logger.info("Training Complete! Returning Model...")
            logger.info(f"Best validation loss achieved: {best_val_loss}")
            print('Log file saved at:', os.path.join(rootDir, f'./Models/{saveModelAs}_files/{saveModelAs}_training.log'))
        if callback:
            callback({
                'message': f"Training Complete! Returning Model..."
            })    
            callback({
                'message': f"Best validation loss achieved: {best_val_loss}"
            })
        
        model.load_state_dict(best_model)
        return model