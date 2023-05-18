# OpenAGI: When LLM Meets Domain Experts

"May the Force be with LLM and Domain Experts." -- Generated by ChatGPT.


<a href='https://arxiv.org/pdf/2304.04370.pdf'><img src='https://img.shields.io/badge/Paper-PDF-red'></a> 
[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)](https://github.com/tatsu-lab/stanford_alpaca/blob/main/LICENSE)

### OpenAGI Framework
<p align="center">
<img src="images/illustration.png" width="800" height="400">
</p>

### Benchmark Task
<p align="center">
<img src="images/pipeline.png" width="800" height="400">
</p>

>An introductory video is available at [here](https://youtu.be/7RaXPPXi0-Y), thanks and credits to @intheworldofai.

## News
-**[2023.5.11]** We release the restructured code of OpenAGI, including the support of both benchmark tasks for quantitative AGI evaluation and open-ended tasks that utilize tools from LangChain, as well as a command line UI that supports easy interaction with OpenAGI when solving complex open-ended tasks.

-**[2023.4.10]** We release the initial version of OpenAGI, including the source code, benchmark, and evaluation methods.

## Introduction
Human intelligence has the remarkable ability to assemble basic skills into complex ones so as to solve complex tasks. This ability is equally important for Artificial Intelligence (AI), and thus, we assert that in addition to the development of large, comprehensive intelligent models, it is equally crucial to equip such models with the capability to harness various domain-specific expert models for complex task-solving in the pursuit of Artificial General Intelligence (AGI). Recent developments in Large Language Models (LLMs) have demonstrated remarkable learning and reasoning abilities, making them promising as a controller to select, synthesize, and execute external models to solve complex tasks. 

This project presents OpenAGI, an open-source AGI research platform, specifically designed to offer complex, multi-step tasks and accompanied by task-specific datasets, evaluation metrics, and a diverse range of extensible models. OpenAGI formulates complex tasks as natural language queries, serving as input to the LLM. The LLM subsequently selects, synthesizes, and executes models provided by OpenAGI to address the task. Furthermore, the project presents the Reinforcement Learning from Task Feedback (RLTF) mechanism, which uses the task-solving result as feedback to improve the LLM's task-solving ability. Thus, the LLM is responsible for synthesizing various external models for solving complex tasks, while RLTF provides feedback to improve its task-solving ability, enabling a feedback loop for self-improving AI. We believe that the paradigm of LLMs operating various expert models for complex task-solving is a promising approach towards AGI. 

To facilitate the community's long-term improvement and evaluation of AGI's ability, we open-source the code, benchmark, and evaluation methods of the OpenAGI project, and we appreciate any discussions, comments, suggestions or contributions from the community.

## Requirements:
- Python 3.9.16
- PyTorch 1.12.1
- transformers==4.28.0
- langchain==0.0.153


## Usage

0. Clone this repo and create a conda virtual environment

    ```
    # create a conda virtual environment
    conda create --name openagi python=3.9
    # actiavte openagi conda environment
    conda activate openagi
    #install torch
    pip3 install torch torchvision torchaudio
    # clone github repo
    git clone https://github.com/agiresearch/OpenAGI.git
    # change directory into project directory
    cd OpenAGI/
    # install required packages
    pip install -r requirements.txt
    ```

1. Download the preprocessed data from this [Google Drive link](https://drive.google.com/drive/folders/1AjT6y7qLIMxcmHhUBG5IE1_5SnCPR57e?usp=share_link), put it into the *OpenAGI/benchmark_tasks/* folder, then unzip it. If you would like to preprocess your own data, please run data_augmentation.py in the *data* folder. Raw data will be automatically downloaded using Hugging Face datasets library; for COCO, please download from [COCO](https://cocodataset.org/#download).

    ```
    wget http://images.cocodataset.org/zips/val2017.zip
    ```


<p align="center">
<img src="images/data_sample.png" width="500" height="500">
</p>



2. To get a teaser of OpenAGI platform, please start by entering the necessary content in the *run_openagi.sh* file.


3. To evaluate Zero-shot or few-show shemas, please change TASK="zero_shot" or TASK="few_shot"   
    ```
    bash run_openagi.sh
    ```
   
4. To evaluate finetuned Flan-T5-Large, please first download the pretrained checkpoints from this [Google Drive link](https://drive.google.com/drive/folders/1AjT6y7qLIMxcmHhUBG5IE1_5SnCPR57e?usp=share_link) into *benchmark_tasks/finetune/* folder, then excute *run_openagi.sh* with TASK="finetune" and LLM_NAME="flan_t5". 
    ```
    bash run_openagi.sh
    ```
    
    Or pretrain with scripts provided in *benchmark_tasks/finetune/* folder to get your own checkpoint, such as

    ```
    python benchmark_tasks/finetune/flan_t5_finetune.py
    ```
 
 5. To evaluate RLTF-based Flan-T5-Large, please first download the pretrained checkpoints from this [Google Drive link](https://drive.google.com/drive/folders/1AjT6y7qLIMxcmHhUBG5IE1_5SnCPR57e?usp=share_link) into *benchmark_tasks/finetune/* folder, then
    ```
    bash run_openagi.sh
    ```
 

## Citation

```
@article{openagi,
  title={OpenAGI: When LLM Meets Domain Experts},
  author={Ge, Yingqiang and Hua, Wenyue and Ji, Jianchao and Tan, Juntao and Xu, Shuyuan and Zhang, Yongfeng},
  journal={arXiv},
  year={2023}
}
```

