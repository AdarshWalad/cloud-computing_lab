# CPU Performance Analysis Using Sysbench on Ubuntu Virtual Machine

[![Course](https://img.shields.io/badge/Course-Cloud%20Computing%20%2F%20Computer%20Networks-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%2022.04.5%20LTS-orange.svg)](#)
[![Benchmark](https://img.shields.io/badge/Benchmark-Sysbench%20CPU%2020k%20Primes-green.svg)](#)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)](#)

---

## Executive Summary

This project presents a practical **CPU performance analysis of an Ubuntu virtual machine** using the `sysbench` benchmarking utility. The experiment measures CPU computational performance using the standard Sysbench CPU prime-number workload with a maximum prime value of **20,000**.

Before running the benchmark, the virtual machine's CPU, memory, storage, and running-process information were examined using standard Linux system-monitoring commands such as `lscpu`, `free -h`, `df -h`, and `top`.

The benchmark was executed using:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

### Key Finding

The virtual machine completed the 10-second CPU benchmark with:

- **17,345 total events**
- **1,734.19 events/sec throughput**
- **0.58 ms average latency**
- **0.63 ms 95th-percentile latency**
- **6.67 ms maximum latency**
- **10.0010 seconds total execution time**

The benchmark used **1 worker thread**.

---

## Table of Contents

1. [Project Objectives](#1-project-objectives)
2. [System Environment](#2-system-environment)
3. [System Resource Analysis](#3-system-resource-analysis)
4. [Experimental Procedure](#4-experimental-procedure)
5. [Sysbench Installation](#5-sysbench-installation)
6. [Benchmark Execution](#6-benchmark-execution)
7. [Empirical Results](#7-empirical-results)
8. [Performance Metrics](#8-performance-metrics)
9. [Technical Analysis](#9-technical-analysis)
10. [Conclusion](#10-conclusion)
11. [Reproduction Steps](#11-reproduction-steps)
12. [Repository Structure](#12-repository-structure)

---

## 1. Project Objectives

The main objectives of this experiment are:

1. **System Identification**  
   Identify the CPU architecture, processor model, number of CPUs, and virtualization environment.

2. **Resource Analysis**  
   Examine available RAM, swap memory, disk capacity, and disk utilization.

3. **Process Monitoring**  
   Use `top` to observe CPU utilization, memory utilization, running tasks, and system load.

4. **Benchmarking**  
   Measure CPU computational performance using the Sysbench CPU benchmark.

5. **Performance Measurement**  
   Collect:
   - Total execution time
   - Total events
   - Events per second
   - Minimum latency
   - Average latency
   - Maximum latency
   - 95th-percentile latency

6. **Performance Interpretation**  
   Analyze what the collected measurements indicate about the CPU and virtualized execution environment.

---

## 2. System Environment

The experiment was performed inside an Ubuntu virtual machine.

### CPU Configuration

The `lscpu` output reports:

| Parameter | Value |
|---|---|
| Architecture | x86_64 |
| CPU op-mode(s) | 32-bit, 64-bit |
| Physical address size | 45 bits |
| Virtual address size | 48 bits |
| Byte Order | Little Endian |
| CPUs | 2 |
| CPU Vendor | GenuineIntel |
| CPU Model | Intel(R) Core(TM) i7-14700 |
| CPU Family | 6 |
| Model | 183 |
| Threads per core | 1 |
| Cores per socket | 2 |
| Sockets | 1 |
| Virtualization | Full |
| Hypervisor Vendor | VMware |
| Virtualization Type | Full |

### Important Observation

Although the underlying processor is an **Intel Core i7-14700**, the experiment is being executed inside a **VMware virtual machine**. Therefore, the benchmark result represents the performance available to the virtual machine rather than a direct bare-metal benchmark of the complete physical CPU.

---

## 3. System Resource Analysis

### 3.1 Memory

The `free -h` output showed approximately:

| Memory Metric | Value |
|---|---:|
| Total RAM | 7.7 GiB |
| Used RAM | 1.7 GiB |
| Free RAM | 4.1 GiB |
| Shared | 44 MiB |
| Buff/Cache | 1.9 GiB |
| Available RAM | 5.7 GiB |
| Swap Total | 2.0 GiB |
| Swap Used | 0 B |

The system had approximately **5.7 GiB of available memory** and **no active swap usage** during the observed state.

### 3.2 Storage

The `df -h` output showed the main filesystem as:

| Parameter | Value |
|---|---:|
| Filesystem | `/dev/sda3` |
| Size | 20 GB |
| Used | 12 GB |
| Available | 6.5 GB |
| Usage | 65% |
| Mount Point | `/` |

This indicates that the virtual machine had sufficient free disk space for the benchmark and Sysbench installation.

### 3.3 Process and CPU Monitoring

The `top` command was used to observe real-time system activity.

The system showed approximately:

- **344 total tasks**
- **1 running task**
- **343 sleeping tasks**
- **0 stopped tasks**
- **0 zombie processes**
- Approximately **97% CPU idle** in the captured system state

This indicates that the system was not under significant general CPU load when the displayed `top` snapshot was captured.

---

## 4. Experimental Procedure

The experiment followed these steps.

### Step 1: Check System Information

The CPU and virtualization environment were identified using:

```bash
lscpu
```

This provided information about:

- CPU architecture
- CPU model
- Number of CPUs
- Cores and threads
- Hypervisor vendor
- Virtualization type
- CPU capabilities

### Step 2: Check Memory

Memory and swap utilization were checked using:

```bash
free -h
```

### Step 3: Check Disk Usage

Filesystem capacity and utilization were checked using:

```bash
df -h
```

### Step 4: Monitor Running Processes

Real-time system activity was monitored using:

```bash
top
```

### Step 5: Install Sysbench

The package repository was updated and Sysbench was installed:

```bash
sudo apt update
sudo apt install sysbench -y
```

### Step 6: Verify Sysbench Version

The installed version was checked using:

```bash
sysbench --version
```

Output:

```text
sysbench 1.0.20
```

### Step 7: Run CPU Benchmark

The CPU benchmark was executed using:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

---

## 5. Sysbench Installation

Sysbench was successfully installed through Ubuntu's package manager.

### Installation Command

```bash
sudo apt install sysbench -y
```

### Version

```text
sysbench 1.0.20
```

Sysbench provides a standardized workload that can be used to evaluate CPU computation performance.

---

## 6. Benchmark Execution

The benchmark command used was:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

### Benchmark Configuration

| Parameter | Value |
|---|---:|
| Benchmark | CPU |
| Maximum Prime | 20,000 |
| Number of Threads | 1 |
| Benchmark Duration | Approximately 10 seconds |
| Sysbench Version | 1.0.20 |

The benchmark generates CPU-intensive prime-number calculations and measures how many operations can be completed during the test.

---

## 7. Empirical Results

The recorded Sysbench result was:

```text
CPU speed:
    events per second: 1734.19

General statistics:
    total time:                  10.0010s
    total number of events:      17345

Latency (ms):
    min:                         0.55
    avg:                         0.58
    max:                         6.67
    95th percentile:             0.63
    sum:                         9993.77

Threads fairness:
    events (avg/stddev):         17345.0000/0.00
    execution time (avg/stddev): 9.9938/0.00
```

### Performance Summary

| Performance Metric | Result |
|---|---:|
| CPU Throughput | **1,734.19 events/sec** |
| Total Events | **17,345** |
| Total Execution Time | **10.0010 sec** |
| Minimum Latency | **0.55 ms** |
| Average Latency | **0.58 ms** |
| 95th Percentile Latency | **0.63 ms** |
| Maximum Latency | **6.67 ms** |
| Latency Sum | **9,993.77 ms** |
| Threads | **1** |

---

## 8. Performance Metrics

### 8.1 Events Per Second

**Events per second (EPS)** represents the number of benchmark operations completed every second.

For this experiment:

```text
Events/sec = 1734.19
```

A higher EPS generally indicates greater CPU throughput for the particular workload being tested.

### 8.2 Total Events

Total events represent the number of benchmark operations completed during the test.

```text
Total Events = 17,345
```

Because the benchmark ran for approximately 10 seconds, the total event count corresponds closely to the measured events-per-second throughput.

### 8.3 Average Latency

Average latency represents the average time required to complete an individual benchmark event.

```text
Average Latency = 0.58 ms
```

Lower latency generally indicates that individual operations are completing faster.

### 8.4 95th Percentile Latency

The 95th percentile indicates the latency value below which approximately 95% of measured operations completed.

```text
95th Percentile = 0.63 ms
```

This metric is useful because an average alone may hide occasional slower operations.

### 8.5 Maximum Latency

Maximum latency represents the slowest recorded event:

```text
Maximum Latency = 6.67 ms
```

The difference between the average latency and maximum latency indicates that a small number of operations experienced substantially higher delays.

---

## 9. Technical Analysis

### 9.1 CPU Throughput

The measured throughput was:

```text
1734.19 events/sec
```

This means that, under the specified Sysbench workload and single-thread configuration, the VM completed approximately **1,734 prime-calculation events every second**.

### 9.2 Single-Threaded Benchmark

An important characteristic of this experiment is:

```text
Number of threads: 1
```

Although the virtual machine reports **2 CPUs**, only one worker thread was used by the benchmark.

Therefore, this experiment primarily measures **single-thread CPU performance** rather than the full multi-core throughput of the virtual machine.

A multi-threaded experiment would be required to evaluate how performance scales when both available CPUs are utilized.

### 9.3 Latency Behavior

The average latency was only:

```text
0.58 ms
```

while the maximum latency reached:

```text
6.67 ms
```

This suggests that most operations completed within a relatively small latency range, while a small number of operations experienced larger delays.

Possible contributors to occasional latency spikes in a virtualized environment include:

- Virtual CPU scheduling
- Host operating-system activity
- Hypervisor scheduling
- Background processes
- Interrupts
- Resource contention

The benchmark result alone does not identify which specific factor caused the maximum-latency spike.

### 9.4 Virtualization Environment

The `lscpu` output identifies:

```text
Hypervisor vendor: VMware
Virtualization type: full
```

Therefore, the benchmark was performed inside a VMware-managed virtual machine.

The result should consequently be interpreted as the performance of the **VM + guest OS + virtualization environment**, rather than as an isolated measurement of the physical Intel i7-14700 processor.

---

## 10. Conclusion

The experiment successfully demonstrated how Linux system utilities and Sysbench can be used to analyze CPU performance inside a virtual machine.

The main observations were:

1. The VM exposes **2 virtual CPUs** based on an Intel Core i7-14700 host processor.
2. The virtualization environment was identified as **VMware**.
3. The VM had approximately **7.7 GiB RAM** and **2 GiB swap**.
4. The main filesystem had a capacity of approximately **20 GB**.
5. Sysbench **1.0.20** was successfully installed.
6. The CPU benchmark used a maximum prime value of **20,000**.
7. The benchmark used **1 worker thread**.
8. The benchmark achieved **1,734.19 events/sec**.
9. The average latency was **0.58 ms**.
10. The 95th-percentile latency was **0.63 ms**.
11. The maximum observed latency was **6.67 ms**.

Overall, the experiment provides a baseline measurement of CPU performance for the configured VMware Ubuntu virtual machine.

---

## 11. Reproduction Steps

### 1. Update Package Repository

```bash
sudo apt update
```

### 2. Install Sysbench

```bash
sudo apt install sysbench -y
```

### 3. Verify Installation

```bash
sysbench --version
```

Expected:

```text
sysbench 1.0.20
```

### 4. Inspect CPU

```bash
lscpu
```

### 5. Inspect Memory

```bash
free -h
```

### 6. Inspect Storage

```bash
df -h
```

### 7. Monitor Processes

```bash
top
```

### 8. Run CPU Benchmark

```bash
sysbench cpu --cpu-max-prime=20000 run
```

---

## 12. Repository Structure

```text
CPU_Performance_Analysis/
│
├── README.md
│
├── images/
│   ├── lscpu.png
│   ├── free_h.png
│   ├── df_h.png
│   ├── top.png
│   ├── sudoapt.png
│   ├── sysbench_version.png
│   └── sysbench_cpu.png
│
└── results/
    └── sysbench_cpu_result.txt
```

### Screenshot Evidence

The repository can include the terminal screenshots used during the experiment:

- `lscpu.png` — CPU and virtualization information
- `free_h.png` — Memory and swap information
- `df_h.png` — Disk usage information
- `top.png` — Process and CPU monitoring
- `sudoapt.png` — Sysbench installation
- `sysbench_version.png` — Sysbench version verification
- `sysbench_cpu.png` — Final CPU benchmark result

---

## Laboratory Experiment

This experiment was conducted as a practical CPU and virtual-machine performance analysis using Linux system monitoring tools and Sysbench.

