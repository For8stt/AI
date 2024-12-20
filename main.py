import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



data = fetch_california_housing()#Sťahovanie a príprava.
X, y = data.data, data.target

scaler_X = StandardScaler()
scaler_y = StandardScaler()

X = scaler_X.fit_transform(X)
y = scaler_y.fit_transform(y.reshape(-1, 1))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

class HousingDataset(Dataset):#uchovania
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

train_dataset = HousingDataset(X_train, y_train)#vytvorenie
test_dataset = HousingDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) #načítanie údajov zo súboru údajov
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

class MLPRegressor(nn.Module): #regresný model
    def __init__(self):
        super(MLPRegressor, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(8, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):# údaje prechádzajú vrstu
        return self.model(x)

def train_model(model, optimizer, criterion, train_loader, test_loader, epochs):
    train_losses, test_losses = [], []

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0

        for X_batch, y_batch in train_loader:
            optimizer.zero_grad() #čistí gradienty
            predictions = model(X_batch).squeeze()#vypočíta predpoveď
            loss = criterion(predictions, y_batch.squeeze()) # stratová funkcia
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        train_losses.append(train_loss / len(train_loader))

        model.eval()
        test_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in test_loader:
                predictions = model(X_batch).squeeze()
                loss = criterion(predictions, y_batch.squeeze())
                test_loss += loss.item()

        test_losses.append(test_loss / len(test_loader))
        print(f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_losses[-1]:.4f}, Test Loss: {test_losses[-1]:.4f}")

    return train_losses, test_losses


def run_experiment(optimizer_name):
    model = MLPRegressor()
    criterion = nn.MSELoss()
    epochs = 100

    if optimizer_name == 'SGD':
        optimizer = optim.SGD(model.parameters(), lr=0.01)
    elif optimizer_name == 'SGD with Momentum':
        optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    elif optimizer_name == 'Adam':
        optimizer = optim.Adam(model.parameters(), lr=0.001)

    print(f"\nTraining with {optimizer_name} optimizer...")
    train_losses, test_losses = train_model(model, optimizer, criterion, train_loader, test_loader, epochs)
    return train_losses, test_losses




if __name__ == '__main__':


    results = {}
    for opt in ['SGD', 'SGD with Momentum', 'Adam']:
        train_losses, test_losses = run_experiment(opt)
        results[opt] = (train_losses, test_losses)

    # plt.figure(figsize=(12, 6))
    # for opt, (train_losses, test_losses) in results.items():
    #     plt.plot(train_losses, label=f'{opt} - Train Loss')
    #     plt.plot(test_losses, label=f'{opt} - Test Loss')
    # plt.xlabel('Epochs')
    # plt.ylabel('Loss')
    # plt.title('Training and Testing Loss by Optimizer')
    # plt.legend()
    # plt.show()
    for opt, (train_losses, test_losses) in results.items():
        plt.figure(figsize=(12, 6))
        plt.plot(train_losses, label=f'{opt} - Train Loss')
        plt.plot(test_losses, label=f'{opt} - Test Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title(f'{opt} - Training and Testing Loss')
        plt.legend()
        plt.show()
