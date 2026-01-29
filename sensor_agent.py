import asyncio
import random
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour

# This class simulates the 'Perception' part of the agent
class MonitorDisaster(PeriodicBehaviour):
    async def run(self):
        # SIMULATED ENVIRONMENT: Sensing disaster data
        # Severity Levels: 0=Normal, 1=Low, 2=Medium, 3=High, 4=Catastrophic
        severities = ["Normal", "Low", "Medium", "High", "Catastrophic"]
        current_percept = random.choice(severities)
        level = severities.index(current_percept)
        
        timestamp = datetime.now().strftime("%H:%M:%S")

        # LOGGING: This satisfies the 'Event Logs' deliverable
        print(f"[{timestamp}] PERCEPT RECEIVED: Damage Level is {current_percept} ({level})")

        # REACTIVE LOGIC: Simple response to perception
        if level >= 3:
            print(f"--- [ALERT] High Severity Detected! Initializing Emergency Protocol ---")

class SensorAgent(Agent):
    async def setup(self):
        print(f"SensorAgent {self.jid} started. Monitoring environment...")
        # Check the environment every 3 seconds
        self.add_behaviour(MonitorDisaster(period=3))

async def main():
    jid = "sensor_agent@localhost"
    password = "password"

    agent = SensorAgent(jid, password)
    
    print("--- [SYSTEM] Connecting to local server... ---")
    
    # REMOVED verify_security to fix the TypeError
    try:
        await agent.start(auto_register=True)
    except Exception as e:
        print(f"Connection failed: {e}")
        return
    
    print("--- [SYSTEM] Monitoring active. Let it run to gather logs... ---")
    
    # Run for 20 seconds so you can capture enough logs for your deliverable
    try:
        await asyncio.sleep(20) 
    except KeyboardInterrupt:
        pass
        
    await agent.stop()
    print("--- [SYSTEM] Monitoring complete. ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass