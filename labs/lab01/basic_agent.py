import asyncio
import sys
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

class MyBehaviour(OneShotBehaviour):
    async def run(self):
        print("\n[SUCCESS] Agent behavior is executing!")
        print(f"Hello from JID: {self.agent.jid}")
        await asyncio.sleep(1)
        await self.agent.stop()

class BasicAgent(Agent):
    async def setup(self):
        print(f"--- Agent {self.jid} is setting up ---")
        self.add_behaviour(MyBehaviour())

async def main():
    # Use localhost for your running PyJabber server
    jid = "student@localhost"
    password = "password"

    print("--- Connecting to local server... ---")
    agent = BasicAgent(jid, password)
    
    # In SPADE 4.x, we disable verify_security by setting it on the agent before start
    # or simply letting it connect to localhost which often skips verification.
    # If it still fails, SPADE 4.x uses 'auto_register' as the primary start arg.
    try:
        await agent.start(auto_register=True)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    print("--- Agent is online! ---")

    while agent.is_alive():
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            await agent.stop()
            break

    print("--- Agent finished. ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass