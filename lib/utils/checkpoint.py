import torch
import numpy as np
import os


class EarlyStopping:
    def __init__(self, patience=7, path="/data/georgia", delta=0):
        self.patience = patience
        self.counter = 0
        self.best_mae = None
        self.best_mse = None
        self.early_stop = False
        self.delta = delta
        self.path = path

    def __call__(self, mse, mae, models):
        if self.best_mae is None:  # first time
            self.best_mae = mae
            self.best_mse = mse
            self.save_checkpoint(models)
        elif (mae > self.best_mae + self.delta) and (mse > self.best_mse + self.delta):
            # both metrics got worse
            self.counter += 1
            print(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_mae = mae
            self.best_mse = mse
            self.save_checkpoint(models)
            self.counter = 0

    def save_checkpoint(self, models):
        if self.path is not None:
            print("Saving model...")
            for name, model in models.items():
                torch.save(
                    model.state_dict(),
                    os.path.join(self.path, "%d_checkpoint.pth" % (name)),
                )
