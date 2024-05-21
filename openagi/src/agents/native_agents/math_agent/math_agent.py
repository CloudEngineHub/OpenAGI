
from ...base import BaseAgent

import os

import sys

from ...agent_process import (
    AgentProcess
)

import argparse

from concurrent.futures import as_completed

import numpy as np

from ....tools.online.currency_converter import CurrencyConverterAPI

from ....tools.online.wolfram_alpha import WolframAlpha

from ....utils.message import Message

import time

import json

import re
class MathAgent(BaseAgent):
    def __init__(self,
                 agent_name,
                 task_input,
                 llm, 
                 agent_process_queue,
                 llm_request_responses,
                 log_mode: str
        ):
        BaseAgent.__init__(self, agent_name, task_input, llm, agent_process_queue, llm_request_responses, log_mode)
        self.tool_list = {
            "wolfram_alpha": WolframAlpha(),
            "currency_converter": CurrencyConverterAPI()
        }
        self.workflow = self.config["workflow"]
        self.tools = self.config["tools"]

    def load_flow(self):
        return

    def run(self):
        prompt = ""
        prefix = self.prefix
        task_input = self.task_input
        prompt += prefix
        request_waiting_times = []
        request_turnaround_times = []
        task_input = "The task you need to solve is: " + task_input
        prompt += task_input

        self.logger.log(f"{task_input}\n", level="info")

        rounds = 0

        # predefined steps
        # TODO replace fixed steps with dynamic steps
        # Step 1 "use a currency converter tool to get the currency information. ",
        # Step 2 "perform mathematical operations using the converted currency amount, which could involve addition, subtraction, multiplication, or division with other numeric values to solve the problem."

        for i, step in enumerate(self.workflow):
            prompt += f"\nIn step {rounds + 1}, you need to {step}. Output should focus on current step and don't be verbose!"
            if i == 0:
                response, start_times, end_times, waiting_times, turnaround_times = self.get_response(
                    message = Message(
                        prompt = prompt,
                        tools = self.tools
                    )
                )
                response_message = response.response_message

                self.set_start_time(start_times[0])

                tool_calls = response.tool_calls

                if tool_calls:
                    self.logger.log(f"***** It starts to call external tools *****\n", level="info")

        prompt += f"Given the interaction history: '{prompt}', integrate solutions in all steps to give a final answer, don't be verbose!"

        output = self.get_response(
            prompt = prompt,
            step = rounds
        )
        final_result = output["response"]

        request_created_times = output["created_times"]

        request_start_times = output["start_times"]

        request_end_times = output["end_times"]
        
        request_waiting_time = [(s - c) for s,c in zip(request_start_times, request_created_times)]

        request_turnaround_time = [(e - c) for e,c in zip(request_end_times, request_created_times)]

        request_waiting_times.extend(request_waiting_time)

        request_turnaround_times.extend(request_turnaround_time)

        self.set_status("done")

        self.set_end_time(time=time.time())

        output = {
            "agent_name": self.agent_name,
            "result": final_result,
            "rounds": rounds,
            "agent_waiting_time": self.start_time - self.created_time,
            "agent_turnaround_time": self.end_time - self.created_time,
            "request_waiting_times": request_waiting_times,
            "request_turnaround_times": request_turnaround_times,
        } 
        self.llm_request_responses[self.get_aid()] = output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run MathAgent')
    parser.add_argument("--agent_name")
    parser.add_argument("--task_input")

    args = parser.parse_args()
    agent = MathAgent(args.agent_name, args.task_input)

    agent.run()
    # thread_pool.submit(agent.run)
    # agent.run()
