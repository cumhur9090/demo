# Overview of Project

Setting up a mini version of the AI agent to be used as a fully functioning demo, on 3 different client profiles with different tool permissions.



## Setup

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Run the agent via the GUI:
   python demo/gui.py

## Features:
- Chatbot that asks you clarifying questions until it can confidently say it understands what the request is / what needs to be done
- Acces to tools: Mail, Settings, Slack
- The agent will have access to prior Convos and get context from it
