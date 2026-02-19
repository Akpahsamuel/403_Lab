"""
LAB 3: GOALS, EVENTS, AND REACTIVE BEHAVIOR
Implementation of a Rescue Agent using Finite State Machine (FSM)

Goals:
1. Monitor disaster zones continuously
2. Respond to high-severity events
3. Coordinate rescue operations
4. Complete rescue missions successfully

FSM States:
- IDLE: Agent is ready but not active
- MONITORING: Continuously monitoring for disasters
- ALERT: High-severity disaster detected
- RESPONDING: Moving to disaster location
- RESCUE: Actively performing rescue operations
- COMPLETED: Mission completed, returning to base
"""

import asyncio
import random
from datetime import datetime
from enum import Enum
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, State, FSMBehaviour
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define FSM States
class States(Enum):
    IDLE = "IDLE"
    MONITORING = "MONITORING"
    ALERT = "ALERT"
    RESPONDING = "RESPONDING"
    RESCUE = "RESCUE"
    COMPLETED = "COMPLETED"

# Define Events that trigger state transitions
class Event:
    def __init__(self, event_type, severity, location=None):
        self.type = event_type
        self.severity = severity
        self.location = location
        self.timestamp = datetime.now()

class IdleState(State):
    async def run(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.CYAN}[{timestamp}] [{States.IDLE.value}] Agent is idle, awaiting activation...{Style.RESET_ALL}")
        await asyncio.sleep(1)
        # Transition to MONITORING
        self.set_next_state(States.MONITORING.value)

class MonitoringState(State):
    async def run(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.GREEN}[{timestamp}] [{States.MONITORING.value}] 🔍 Monitoring disaster zones...{Style.RESET_ALL}")
        
        # Simulate sensor input
        severities = ["Normal", "Low", "Medium", "High", "Catastrophic"]
        severity = random.choice(severities)
        level = severities.index(severity)
        
        print(f"{Fore.BLUE}[{timestamp}] 📊 Sensor Report: Severity = {severity} (Level {level}){Style.RESET_ALL}")
        
        # Store event data in agent
        self.agent.current_event = Event("disaster_detected", level, f"Zone-{random.randint(1, 5)}")
        
        await asyncio.sleep(2)
        
        # Decision: Transition based on severity
        if level >= 3:  # High or Catastrophic
            print(f"{Fore.YELLOW}[{timestamp}] ⚠️  EVENT TRIGGERED: High severity detected!{Style.RESET_ALL}")
            self.set_next_state(States.ALERT.value)
        else:
            # Continue monitoring
            self.set_next_state(States.MONITORING.value)

class AlertState(State):
    async def run(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        event = self.agent.current_event
        print(f"{Fore.RED}{Style.BRIGHT}[{timestamp}] [{States.ALERT.value}] 🚨 ALERT! Emergency at {event.location}!{Style.RESET_ALL}")
        print(f"{Fore.RED}[{timestamp}] 📋 GOAL ACTIVATED: Initiate rescue operation{Style.RESET_ALL}")
        
        await asyncio.sleep(1)
        
        # Transition to RESPONDING
        self.set_next_state(States.RESPONDING.value)

class RespondingState(State):
    async def run(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        event = self.agent.current_event
        print(f"{Fore.MAGENTA}[{timestamp}] [{States.RESPONDING.value}] 🚁 Dispatching to {event.location}...{Style.RESET_ALL}")
        
        # Simulate travel time
        for i in range(3):
            await asyncio.sleep(1)
            print(f"{Fore.MAGENTA}[{timestamp}] 🛣️  En route... ({i+1}/3){Style.RESET_ALL}")
        
        print(f"{Fore.MAGENTA}[{timestamp}] ✅ Arrived at {event.location}{Style.RESET_ALL}")
        
        # Transition to RESCUE
        self.set_next_state(States.RESCUE.value)

class RescueState(State):
    async def run(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        event = self.agent.current_event
        print(f"{Fore.YELLOW}{Style.BRIGHT}[{timestamp}] [{States.RESCUE.value}] 🆘 Performing rescue operation at {event.location}...{Style.RESET_ALL}")
        
        # Simulate rescue operations
        operations = ["Evacuating victims", "Providing medical aid", "Securing perimeter", "Clearing debris"]
        for op in operations:
            await asyncio.sleep(1.5)
            print(f"{Fore.YELLOW}[{timestamp}] 👷 {op}...{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}{Style.BRIGHT}[{timestamp}] ✅ Rescue operation successful!{Style.RESET_ALL}")
        
        # Transition to COMPLETED
        self.set_next_state(States.COMPLETED.value)

class CompletedState(State):
    async def run(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.GREEN}[{timestamp}] [{States.COMPLETED.value}] 🏁 Mission completed successfully!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[{timestamp}] 📊 GOAL ACHIEVED: Rescue operation completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[{timestamp}] 🔄 Returning to monitoring state...{Style.RESET_ALL}")
        
        await asyncio.sleep(2)
        
        # Increment mission counter
        self.agent.missions_completed += 1
        
        # Return to MONITORING for next mission
        if self.agent.missions_completed < self.agent.max_missions:
            self.set_next_state(States.MONITORING.value)
        else:
            # End FSM after max missions
            print(f"{Fore.CYAN}[{timestamp}] 🛑 Maximum missions reached. Agent shutting down.{Style.RESET_ALL}")
            await self.agent.stop()

class RescueAgentFSM(FSMBehaviour):
    async def on_start(self):
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}  RESCUE AGENT FSM - LAB 3: Goals, Events, and Reactive Behavior{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}🎯 Agent Goals:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  1. Monitor disaster zones continuously{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  2. Respond to high-severity events (Level ≥ 3){Style.RESET_ALL}")
        print(f"{Fore.WHITE}  3. Coordinate and execute rescue operations{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  4. Complete missions and return to monitoring{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}📊 FSM States: {[s.value for s in States]}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")

    async def on_end(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[{timestamp}] 📈 FSM Execution Complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[{timestamp}] ✅ Total Missions Completed: {self.agent.missions_completed}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
        await self.agent.stop()

class RescueAgent(Agent):
    async def setup(self):
        print(f"{Fore.CYAN}🤖 RescueAgent {self.jid} initialized{Style.RESET_ALL}\n")
        
        # Agent state variables
        self.current_event = None
        self.missions_completed = 0
        self.max_missions = 2  # Run 2 complete missions for demo
        
        # Create FSM behaviour
        fsm = RescueAgentFSM()
        
        # Add states to FSM
        fsm.add_state(States.IDLE.value, IdleState(), initial=True)
        fsm.add_state(States.MONITORING.value, MonitoringState())
        fsm.add_state(States.ALERT.value, AlertState())
        fsm.add_state(States.RESPONDING.value, RespondingState())
        fsm.add_state(States.RESCUE.value, RescueState())
        fsm.add_state(States.COMPLETED.value, CompletedState())
        
        # Define state transitions
        fsm.add_transition(States.IDLE.value, States.MONITORING.value)
        fsm.add_transition(States.MONITORING.value, States.MONITORING.value)
        fsm.add_transition(States.MONITORING.value, States.ALERT.value)
        fsm.add_transition(States.ALERT.value, States.RESPONDING.value)
        fsm.add_transition(States.RESPONDING.value, States.RESCUE.value)
        fsm.add_transition(States.RESCUE.value, States.COMPLETED.value)
        fsm.add_transition(States.COMPLETED.value, States.MONITORING.value)
        
        self.add_behaviour(fsm)

async def main():
    jid = "rescue_agent@localhost"
    password = "password"

    agent = RescueAgent(jid, password)
    
    try:
        await agent.start(auto_register=True)
        print(f"{Fore.GREEN}✅ Agent connected to XMPP server{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Connection failed: {e}{Style.RESET_ALL}")
        return
    
    # Keep agent running
    while agent.is_alive():
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break
    
    await agent.stop()
    print(f"\n{Fore.CYAN}Agent shutdown complete.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program interrupted by user{Style.RESET_ALL}")
