
from ...base import BaseAgent

import time

from ...agent_process import (
    AgentProcess
)

import argparse

from concurrent.futures import as_completed

import numpy as np
class RecAgent(BaseAgent):
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
            
        }
        self.tool_check_max_fail_times = 10
        self.tool_select_max_fail_times = 10
        self.tool_calling_max_fail_times = 10
        self.tool_info = "".join(self.config["tool_info"])

    def run(self):
        prompt = ""
        prefix = self.prefix
        prompt += prefix
        task_input = self.task_input
        task_input = "The task you need to solve is: " + task_input
        self.logger.log(f"{task_input}\n", level="info")
        prompt += task_input
        request_waiting_times = []
        request_turnaround_times = []

        procedures = [
            "give a general recommendation direction for users.",
            "based on the above recommendation direction, give a recommendation list."
        ]

        rounds = 0

        for i, p in enumerate(procedures):
            prompt += f"\nIn step {rounds+1}, you need to {p}. Output should focus on current step and don't be verbose!"

            self.logger.log(f"Step {i+1}: {p}\n", level="info")

            output = self.get_response(
                prompt = prompt,
                step = rounds
            )

            response = output["response"]

            request_created_times = output["created_times"]

            request_start_times = output["start_times"]

            request_end_times = output["end_times"]

            request_waiting_time = [(s - c) for s,c in zip(request_start_times, request_created_times)]

            request_turnaround_time = [(e - c) for e,c in zip(request_end_times, request_created_times)]

            request_waiting_times.extend(request_waiting_time)

            request_turnaround_times.extend(request_turnaround_time)

            if rounds == 0:
                self.set_start_time(output["start_times"][0])
            
            self.logger.log(
                f"Solution for current step {rounds+1} is: {response}\n",
                level="info"
            )

            rounds += 1

        prompt += f"Given the interaction history: '{prompt}', give a final recommendation list and explanations, don't be verbose!"

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

        self.logger.log(
            f"{task_input} Final result is: {final_result}\n",
            level="info"
        )
        
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

    def parse_result(self, prompt):
        return prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run NarrativeAgent')
    parser.add_argument("--agent_name")
    parser.add_argument("--task_input")

    args = parser.parse_args()
    agent = RecAgent(args.agent_name, args.task_input)
    agent.run()
