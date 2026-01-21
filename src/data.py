# src/data.py
# xAI/x Simulation - Newtonian Physics Data Engine

import torch
import numpy as np
import tqdm as tqdm
import os
from pathlib import Path

class PhysicsDataEngine:
    def __init__(self, num_trajectories: int = 10_000, seq_len: int = 100, dt: float = 0.1, device: str = "mps" if torch.backends.mps.is_available() else "cpu"):
        self.num_trajectories = num_trajectories
        self.seq_len = seq_len
        self.dt = dt
        self.device = device 
        print(f"PhysicsDataEngine initialized on {self.device.upper()}")
    
    def simulate_trajectory(self, seed: int = 0):
        """simulate one 2D trajectory under Newtonian physics + noise"""
        torch.manual_seed(seed)
        np.random.seed(seed)

        # random physical parameters
        mass = torch.rand(1) * 5.0 + 1.0 # 1 to 6 kg 
        gravity = torch.tensor([0.0, -9.81]) # m/ssquared
        drag_coeff = torch.rand(1) * 0.5 # air resistance
        wind_force = torch.randn(2) * 10.0 # initial velocity
    
        # initial conditions
        pos = torch.randn(2) * 5.0 # start within [-5, 5]
        vel = torch.randn(2) * 10.0 # initial velocity
    
        trajectory = []
        for _ in range(self.seq_len):
            # forces
            F_gravity = mass * gravity 
            F_drag = -drag_coeff * vel * torch.norm(vel)
            F_wind = wind_force
            F_total = F_gravity + F_drag + F_wind

            # newton: F= ma-> a = F/m
            acc = F_total / mass

            # euler integration
            vel = vel + acc * self.dt
            pos = pos + vel * self.dt

            # add observation noise
            pos_noisy = pos + torch.randn(2) * 0.05

            trajectory.append(pos_noisy.clone())
        return torch.stack(trajectory), {'mass': mass.item(), 'drag_coeff': drag_coeff.item(), 'wind_force': wind_force.tolist(), 'initial_velocity': vel.tolist(), 'seed': seed}
    
    def generate_dataset(self, save_path: str = "./data/physics_v1.pt"):
        """generate full dataset and save with metadata"""
        os.makedirs("data", exist_ok=True)
        
        trajectories = []
        metadata = []
        print(f'Generating {self.num_trajectories} trajectories...')
        for i in tqdm.tqdm(range(self.num_trajectories)):
            traj, meta = self.simulate_trajectory(seed=i)
            trajectories.append(traj)
            metadata.append(meta)

        # stack [N, T, 2]
        data = torch.stack(trajectories).to(self.device)
        print(f'dataset shape: {data.shape}')

        # save
        torch.save({'data': data.cpu(), 'metadata': metadata, 'config': {'num_trajectories': self.num_trajectories, 'seq_len': self.seq_len, 'dt': self.dt, 'description': "2D newtonian motion with gravity, drag, wind, noise"}}, save_path)

        print(f'Saved to {save_path}')
        return data, metadata
    
    # run once to generate data
if __name__ == "__main__":
    engine = PhysicsDataEngine()
    data, meta = engine.generate_dataset()


