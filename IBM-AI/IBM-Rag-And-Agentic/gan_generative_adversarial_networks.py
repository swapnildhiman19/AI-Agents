import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# ============================================================
# STEP 1: Define the Generator
# Takes random noise (latent vector z) and transforms it
# into something that looks like real data.
# Architecture: Noise(100) -> 256 -> 512 -> 1024 -> 784 (28x28 image)
# ============================================================
class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_dim=784):
        super().__init__()
        self.model = nn.Sequential(
        nn.Linear(latent_dim, 256),   # 100 -> 256
        nn.LeakyReLU(0.2),

        nn.Linear(256, 512),          # 256 -> 512
        nn.LeakyReLU(0.2),

        nn.Linear(512, 1024),         # 512 -> 1024  ← THIS WAS THE BUG
        nn.LeakyReLU(0.2),

        nn.Linear(1024, img_dim),     # 1024 -> 784
        nn.Tanh(),
    )
    def forward(self, z):
        # z shape: (batch_size, 100) -> output shape: (batch_size, 784)
        return self.model(z)

# ============================================================
# STEP 2: Define the Discriminator
# Takes an image (real or fake) and outputs a probability
# that the image is real (1 = real, 0 = fake).
# Architecture: 784 -> 1024 -> 512 -> 256 -> 1
# ============================================================
class Discriminator(nn.Module):
    def __init__(self, img_dim=784):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(img_dim, 1024),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),             # Dropout prevents D from becoming too strong
            
            nn.Linear(1024, 512),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            
            nn.Linear(256, 1),
            nn.Sigmoid()                 # Sigmoid outputs probability [0, 1]
        )
    
    def forward(self, x):
        return self.model(x)

# ============================================================
# STEP 3: Training Loop — The Adversarial Game
# ============================================================
latent_dim = 100
lr = 0.0002

G = Generator(latent_dim)
D = Discriminator()

# Both use Adam optimizer — standard for GANs
optimizer_G = optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
optimizer_D = optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))

criterion = nn.BCELoss()  # Binary Cross Entropy — perfect for real/fake classification

# Simulating training (pseudo-code for one batch):
batch_size = 64

# --- Train Discriminator ---
# Goal: maximize log(D(real)) + log(1 - D(G(z)))
real_data = torch.randn(batch_size, 784)  # Placeholder for real images
real_labels = torch.ones(batch_size, 1)    # Label = 1 for real
fake_labels = torch.zeros(batch_size, 1)   # Label = 0 for fake

# D on real data
real_output = D(real_data)
d_loss_real = criterion(real_output, real_labels)

# D on fake data
z = torch.randn(batch_size, latent_dim)    # Random noise
fake_data = G(z)                            # G generates fake images
fake_output = D(fake_data.detach())         # .detach() stops gradients flowing to G
d_loss_fake = criterion(fake_output, fake_labels)

d_loss = d_loss_real + d_loss_fake          # Total D loss
optimizer_D.zero_grad()
d_loss.backward()
optimizer_D.step()

# --- Train Generator ---
# Goal: minimize log(1 - D(G(z))) ≡ maximize log(D(G(z)))
z = torch.randn(batch_size, latent_dim)
fake_data = G(z)
fake_output = D(fake_data)                  # No .detach() — we WANT gradients to flow to G
g_loss = criterion(fake_output, real_labels) # G wants D to think fakes are real
optimizer_G.zero_grad()
g_loss.backward()
optimizer_G.step()

print(f"D Loss: {d_loss.item():.4f} | G Loss: {g_loss.item():.4f}")