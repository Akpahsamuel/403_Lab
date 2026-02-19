"""
LAB 4: AGENT COMMUNICATION USING FIPA-ACL
Underground Hacker Collective - Multi-Agent Communication System

Scenario:
A collective of autonomous hacker agents coordinate cyber operations using
secure FIPA-ACL messaging to discover vulnerabilities, execute exploits,
and monitor security threats.

Agents:
1. ReconAgent - Scans systems, discovers vulnerabilities, INFORMs collective
2. MainHackerAgent - Coordinates operations, REQUESTs specific attacks
3. WatchdogAgent - Monitors security heat, INFORMs threat levels

FIPA-ACL Performatives Used:
- INFORM: Share intelligence, status updates, alerts
- REQUEST: Ask for specific actions, data, or exploits
"""

import asyncio
import random
import json
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Message logger
MESSAGE_LOG = []

def log_message(sender, receiver, performative, content):
    """Log all ACL messages for deliverable"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "from": sender,
        "to": receiver,
        "performative": performative,
        "content": content
    }
    MESSAGE_LOG.append(log_entry)
    return log_entry


class ReconBehaviour(CyclicBehaviour):
    """Reconnaissance agent that scans for vulnerabilities and reports findings"""
    
    async def run(self):
        # Scan for targets
        targets = [
            {"type": "database", "name": "FinanceCorp SQL", "vuln": "SQL Injection", "value": "high"},
            {"type": "server", "name": "GovServer-42", "vuln": "Unpatched CVE", "value": "critical"},
            {"type": "network", "name": "Corp-WiFi", "vuln": "Weak encryption", "value": "medium"},
            {"type": "api", "name": "PaymentAPI", "vuln": "Auth bypass", "value": "high"},
            {"type": "webapp", "name": "AdminPanel", "vuln": "Default creds", "value": "low"},
        ]
        
        await asyncio.sleep(random.uniform(3, 6))
        
        target = random.choice(targets)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n{Fore.CYAN}[{timestamp}] [{self.agent.agent_name}] 🔍 Scanning network...")
        print(f"{Fore.GREEN}[{timestamp}] [{self.agent.agent_name}] ✓ Target discovered: {target['name']}")
        print(f"{Fore.YELLOW}[{timestamp}] [{self.agent.agent_name}] 📊 Vulnerability: {target['vuln']} (Value: {target['value']})")
        
        # Send INFORM message to MainHacker
        msg = Message(to="main_hacker@localhost")
        msg.set_metadata("performative", "inform")
        msg.body = json.dumps({
            "action": "target_discovered",
            "target": target,
            "timestamp": timestamp
        })
        
        await self.send(msg)
        log_message(self.agent.agent_name, "main_hacker", "INFORM", f"Target discovered: {target['name']}")
        
        print(f"{Fore.MAGENTA}[{timestamp}] [{self.agent.agent_name}] 📤 INFORM sent to MainHacker about {target['name']}")


class MainHackerBehaviour(CyclicBehaviour):
    """Main coordinator that receives intel and requests specific operations"""
    
    async def run(self):
        # Wait for messages
        msg = await self.receive(timeout=10)
        
        if msg:
            timestamp = datetime.now().strftime("%H:%M:%S")
            performative = msg.get_metadata("performative")
            sender = str(msg.sender).split("@")[0]
            
            try:
                data = json.loads(msg.body)
                
                if performative == "inform":
                    if data.get("action") == "target_discovered":
                        target = data["target"]
                        print(f"\n{Fore.BLUE}[{timestamp}] [MainHacker] 📨 INFORM received from {sender}")
                        print(f"{Fore.BLUE}[{timestamp}] [MainHacker] 📋 Intel: {target['name']} - {target['vuln']}")
                        
                        # Decide whether to exploit based on value
                        if target['value'] in ['high', 'critical']:
                            print(f"{Fore.RED}[{timestamp}] [MainHacker] 🎯 High-value target! Initiating operation...")
                            
                            # REQUEST Watchdog for heat level check
                            request_msg = Message(to="watchdog@localhost")
                            request_msg.set_metadata("performative", "request")
                            request_msg.body = json.dumps({
                                "action": "check_heat_level",
                                "target": target['name']
                            })
                            
                            await self.send(request_msg)
                            log_message("main_hacker", "watchdog", "REQUEST", "Check heat level for operation")
                            
                            print(f"{Fore.MAGENTA}[{timestamp}] [MainHacker] 📤 REQUEST sent to Watchdog: Check heat level")
                            
                            # Increase operation counter
                            self.agent.operations_planned += 1
                        else:
                            print(f"{Fore.YELLOW}[{timestamp}] [MainHacker] ⏭️  Low-value target, skipping...")
                    
                    elif data.get("action") == "heat_status":
                        heat_level = data["heat_level"]
                        status = data["status"]
                        
                        print(f"\n{Fore.BLUE}[{timestamp}] [MainHacker] 📨 INFORM received from {sender}")
                        print(f"{Fore.BLUE}[{timestamp}] [MainHacker] 🌡️  Heat Level: {heat_level}% - Status: {status}")
                        
                        if heat_level < 70:
                            print(f"{Fore.GREEN}[{timestamp}] [MainHacker] ✅ Proceeding with exploit...")
                            self.agent.operations_executed += 1
                            
                            # Simulate exploit
                            success = random.choice([True, True, True, False])  # 75% success rate
                            if success:
                                print(f"{Fore.GREEN}{Style.BRIGHT}[{timestamp}] [MainHacker] 💰 EXPLOIT SUCCESSFUL! Data exfiltrated.")
                                self.agent.successful_ops += 1
                            else:
                                print(f"{Fore.RED}[{timestamp}] [MainHacker] ❌ Exploit failed, target detected intrusion.")
                        else:
                            print(f"{Fore.RED}[{timestamp}] [MainHacker] 🚨 ABORT! Heat too high, operation cancelled.")
                
            except json.JSONDecodeError:
                print(f"{Fore.RED}[{timestamp}] [MainHacker] ⚠️  Malformed message received")


class WatchdogBehaviour(CyclicBehaviour):
    """Security monitor that tracks heat levels and responds to requests"""
    
    async def run(self):
        msg = await self.receive(timeout=10)
        
        if msg:
            timestamp = datetime.now().strftime("%H:%M:%S")
            performative = msg.get_metadata("performative")
            sender = str(msg.sender).split("@")[0]
            
            try:
                data = json.loads(msg.body)
                
                if performative == "request" and data.get("action") == "check_heat_level":
                    print(f"\n{Fore.CYAN}[{timestamp}] [Watchdog] 📨 REQUEST received from {sender}")
                    print(f"{Fore.CYAN}[{timestamp}] [Watchdog] 🔍 Analyzing security posture...")
                    
                    await asyncio.sleep(1)
                    
                    # Calculate heat level
                    heat_level = random.randint(20, 95)
                    self.agent.current_heat = heat_level
                    
                    if heat_level < 50:
                        status = "SAFE"
                        color = Fore.GREEN
                    elif heat_level < 70:
                        status = "ELEVATED"
                        color = Fore.YELLOW
                    else:
                        status = "CRITICAL"
                        color = Fore.RED
                    
                    print(f"{color}[{timestamp}] [Watchdog] 🌡️  Heat Level: {heat_level}% - {status}")
                    
                    # Send INFORM response
                    response_msg = Message(to="main_hacker@localhost")
                    response_msg.set_metadata("performative", "inform")
                    response_msg.body = json.dumps({
                        "action": "heat_status",
                        "heat_level": heat_level,
                        "status": status
                    })
                    
                    await self.send(response_msg)
                    log_message("watchdog", "main_hacker", "INFORM", f"Heat level: {heat_level}% - {status}")
                    
                    print(f"{Fore.MAGENTA}[{timestamp}] [Watchdog] 📤 INFORM sent to MainHacker with heat status")
                    
                    # If critical, send warning to all
                    if heat_level >= 85:
                        print(f"{Fore.RED}{Style.BRIGHT}[{timestamp}] [Watchdog] 🚨 ALERT: Critical heat detected!")
                        self.agent.alerts_sent += 1
                        
            except json.JSONDecodeError:
                print(f"{Fore.RED}[{timestamp}] [Watchdog] ⚠️  Malformed message received")


class ReconAgent(Agent):
    """Reconnaissance agent that discovers targets"""
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.agent_name = "ReconAgent"
    
    async def setup(self):
        print(f"{Fore.CYAN}🔍 {self.agent_name} initialized - Awaiting orders...{Style.RESET_ALL}")
        recon_behaviour = ReconBehaviour()
        self.add_behaviour(recon_behaviour)


class MainHackerAgent(Agent):
    """Main coordinator agent"""
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.operations_planned = 0
        self.operations_executed = 0
        self.successful_ops = 0
    
    async def setup(self):
        print(f"{Fore.RED}💀 MainHacker initialized - Command center online{Style.RESET_ALL}")
        main_behaviour = MainHackerBehaviour()
        self.add_behaviour(main_behaviour)


class WatchdogAgent(Agent):
    """Security monitoring agent"""
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.current_heat = 0
        self.alerts_sent = 0
    
    async def setup(self):
        print(f"{Fore.YELLOW}🛡️  Watchdog initialized - Monitoring security infrastructure{Style.RESET_ALL}")
        watchdog_behaviour = WatchdogBehaviour()
        self.add_behaviour(watchdog_behaviour)


async def main():
    print(f"{Fore.RED}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}  UNDERGROUND HACKER COLLECTIVE - LAB 4: FIPA-ACL Communication{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}⚡ Scenario: Autonomous hacker agents coordinate cyber operations")
    print(f"{Fore.WHITE}📡 Protocol: FIPA-ACL with INFORM and REQUEST performatives\n")
    print(f"{Fore.WHITE}🤖 Agents:")
    print(f"{Fore.CYAN}  • ReconAgent - Discovers vulnerabilities (INFORM)")
    print(f"{Fore.RED}  • MainHacker - Coordinates operations (REQUEST)")
    print(f"{Fore.YELLOW}  • Watchdog - Monitors security heat (INFORM/REQUEST)")
    print(f"{Fore.WHITE}\n{'='*80}\n{Style.RESET_ALL}")
    
    # Create agents
    recon = ReconAgent("recon@localhost", "password")
    hacker = MainHackerAgent("main_hacker@localhost", "password")
    watchdog = WatchdogAgent("watchdog@localhost", "password")
    
    # Start all agents
    try:
        await recon.start(auto_register=True)
        await hacker.start(auto_register=True)
        await watchdog.start(auto_register=True)
        print(f"{Fore.GREEN}✅ All agents connected to XMPP server\n{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Connection failed: {e}{Style.RESET_ALL}")
        return
    
    # Run for demo period
    print(f"{Fore.MAGENTA}🚀 Collective operational - Running for 40 seconds...\n{Style.RESET_ALL}")
    await asyncio.sleep(40)
    
    # Shutdown
    print(f"\n{Fore.YELLOW}⏹️  Initiating shutdown sequence...{Style.RESET_ALL}")
    await recon.stop()
    await hacker.stop()
    await watchdog.stop()
    
    # Print summary
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}  OPERATION SUMMARY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}📊 Statistics:")
    print(f"{Fore.WHITE}  • Operations Planned: {hacker.operations_planned}")
    print(f"{Fore.WHITE}  • Operations Executed: {hacker.operations_executed}")
    print(f"{Fore.GREEN}  • Successful Exploits: {hacker.successful_ops}")
    print(f"{Fore.YELLOW}  • Security Alerts: {watchdog.alerts_sent}")
    print(f"{Fore.MAGENTA}  • Total Messages: {len(MESSAGE_LOG)}\n")
    
    # Print message log
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  MESSAGE LOG (FIPA-ACL){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    for log in MESSAGE_LOG:
        print(f"[{log['timestamp']}] {log['from']} → {log['to']}")
        print(f"  Performative: {log['performative']}")
        print(f"  Content: {log['content']}\n")
    
    print(f"{Fore.GREEN}✅ All agents disconnected. Collective offline.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Emergency shutdown initiated by operator{Style.RESET_ALL}")
