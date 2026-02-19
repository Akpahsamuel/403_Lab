import asyncio
import random
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

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
        # Color coding based on severity
        if level == 0:
            color = Fore.GREEN
        elif level == 1:
            color = Fore.BLUE
        elif level == 2:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        
        print(f"{color}[{timestamp}] PERCEPT RECEIVED: Damage Level is {current_percept} ({level}){Style.RESET_ALL}")

        # REACTIVE LOGIC: Simple response to perception
        if level >= 3:
            print(f"{Fore.RED}{Style.BRIGHT}--- [ALERT] High Severity Detected! Initializing Emergency Protocol ---{Style.RESET_ALL}")

class SensorAgent(Agent):
    async def setup(self):
        print(f"{Fore.CYAN}SensorAgent {self.jid} started. Monitoring environment...{Style.RESET_ALL}")
        # Check the environment every 3 seconds
        self.add_behaviour(MonitorDisaster(period=3))

async def main():
    jid = "sensor_agent@localhost"
    password = "password"

    agent = SensorAgent(jid, password)
    
    print(f"{Fore.CYAN}--- [SYSTEM] Connecting to local server... ---{Style.RESET_ALL}")
    
    # REMOVED verify_security to fix the TypeError
    try:
        await agent.start(auto_register=True)
    except Exception as e:
        print(f"{Fore.RED}Connection failed: {e}{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}--- [SYSTEM] Monitoring active. Let it run to gather logs... ---{Style.RESET_ALL}")
    
    # Run for 20 seconds so you can capture enough logs for your deliverable
    try:
        await asyncio.sleep(20) 
    except KeyboardInterrupt:
        pass
        
    await agent.stop()
    print(f"{Fore.CYAN}--- [SYSTEM] Monitoring complete. ---{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass