# spanish-author-profiler

Spanish-author-profiler is a tool that lets you analyze, using automatic author profiling techniques, large corpuses of Spanish speaking users based on their posts in social media. Author profiling consists in the automatic extraction of author traits like age and gender based on their redaction style.

https://github.com/nmiguezg/spanish-author-profiler/assets/72253608/83f4354e-521a-473b-bb04-3056d26390c5

## Features

Currently, this tool supports the following features:

- Uploading files containing large collections of **Spanish-speaking social media users** with their posts.
- Profiling of **demographic traits** like age and gender.
- Selection of multiple **spanish author profiling algorithms**.
- **Interactive dashboard** for analyzing the profiled users corpus including:
  - Charts for visualizing the **profiled categories distribution** in the dataset.
  - Collection's **users full list** for accessing individual information about each one.
  - **Filtering** based on inferred categories like age or gender.
- Detailed visualization of individual **posts and user information**.
- **Historic of profiled corpuses** for accessing their respective dashboard at any time.
- Intuitive and **responsive interface**, for accessing the tool in any device, independently form its resolution.

> **Note:** The two modules: [magic](./profilers-sevice/magic) and [pan](./profilers-sevice/pan) are adaptations from [modaresi16](<https://github.com/pan-webis-de/modaresi16>) and [grivas15](<https://github.com/pan-webis-de/grivas15>), respectively. The credit for the development of these author profiling modules goes to their respective authors.

## Pre-requisites

- Docker
- docker-compose

## Installation

```bash
git lfs install
git clone git@github.com:nmiguezg/spanish-author-profiler.git
cd spanish-author-profiler
git lfs pull
docker-compose up --build -d
```

Then, the tool can be accessed by navigating to [http://localhost:3000](http://localhost:3000).
