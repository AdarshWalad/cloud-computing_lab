# Lab Report: Performance Analysis of Type-1 and Type-2 Hypervisors

## Cloud Computing / Computer Networks

---

## 1. Title

**Performance Analysis of Type-1 and Type-2 Hypervisors Using Sysbench CPU Benchmark**

---

## 2. Objective

The objectives of this experiment are:

1. To compare the CPU performance of a **Type-1 bare-metal hypervisor** and a **Type-2 hosted hypervisor**.
2. To execute the same Sysbench CPU workload in both virtual machines.
3. To measure CPU throughput and latency.
4. To compare the total number of CPU benchmark events completed.
5. To analyze the performance overhead associated with the two virtualization architectures.

---

## 3. Introduction

A hypervisor is software that enables multiple virtual machines (VMs) to share the resources of a physical computer.

Hypervisors can broadly be classified into two categories:

### Type-1 Hypervisor

A Type-1 hypervisor, also called a **bare-metal hypervisor**, runs directly on the physical hardware.

```text
Physical Hardware
       ↓
Type-1 Hypervisor
       ↓
Virtual Machine
       ↓
Guest Operating System
```

Examples include:

- Proxmox VE
- VMware ESXi
- Microsoft Hyper-V

### Type-2 Hypervisor

A Type-2 hypervisor runs as an application on top of a host operating system.

```text
Physical Hardware
       ↓
Host Operating System
       ↓
Type-2 Hypervisor
       ↓
Virtual Machine
       ↓
Guest Operating System
```

Examples include:

- VMware Workstation
- Oracle VirtualBox

The experiment uses **Proxmox VE** as the Type-1 environment and **VMware Workstation** as the Type-2 environment.

---

## 4. Experimental Setup

The experiment compares two virtualized environments using the same CPU benchmark workload.

| Parameter | Type-1 | Type-2 |
|---|---|---|
| Hypervisor | Proxmox VE | VMware Workstation |
| Hypervisor Type | Bare-Metal | Hosted |
| Guest OS | Ubuntu | Ubuntu |
| CPU Benchmark | Sysbench CPU | Sysbench CPU |
| Maximum Prime | 20,000 | 20,000 |
| Benchmark Duration | ~10 seconds | ~10 seconds |
| CPU Workload | Same | Same |

The benchmark is intended to provide a common workload so that the resulting throughput and latency values can be compared.

---

## 5. Software and Tools

### Sysbench

**Sysbench** is a benchmarking utility used to evaluate system performance.

For this experiment, its CPU benchmark was used:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

The benchmark performs prime-number calculations and reports CPU throughput and latency statistics.

### Linux Monitoring Commands

The following commands can be used to inspect the virtual machine before benchmarking:

```bash
lscpu
```

```bash
free -h
```

```bash
df -h
```

```bash
top
```

---

## 6. Experimental Procedure

### Step 1: Configure the Virtual Machines

Two Ubuntu virtual machines were configured for the comparison:

- One running under **Proxmox VE**
- One running under **VMware Workstation**

The benchmark workload was kept the same.

### Step 2: Verify System Configuration

CPU information:

```bash
lscpu
```

Memory information:

```bash
free -h
```

Disk information:

```bash
df -h
```

Process and CPU monitoring:

```bash
top
```

### Step 3: Install Sysbench

```bash
sudo apt update
sudo apt install sysbench -y
```

### Step 4: Verify Installation

```bash
sysbench --version
```

### Step 5: Execute the CPU Benchmark

```bash
sysbench cpu --cpu-max-prime=20000 run
```

### Step 6: Record the Results

The following metrics were collected:

- Events per second
- Total events
- Minimum latency
- Average latency
- 95th-percentile latency
- Maximum latency

---

# 7. Experimental Results

## 7.1 CPU Throughput

The measured CPU throughput was:

| Hypervisor | Type | Throughput |
|---|---|---:|
| Proxmox VE | Type-1 | **1,716.69 events/sec** |
| VMware Workstation | Type-2 | **1,364.78 events/sec** |

Proxmox VE achieved a higher CPU throughput in the recorded experiment.

### Throughput Comparison

![CPU Throughput Comparison](images/cpu_throughput_comparison.jpeg)

**Figure 1: CPU throughput comparison using the Sysbench 20k-prime workload.**

According to the recorded result, Proxmox VE achieved approximately **25.79% higher CPU throughput** than VMware Workstation.

---

## 7.2 Latency Comparison

The recorded latency values were:

| Latency Metric | Proxmox VE | VMware Workstation |
|---|---:|---:|
| Minimum | **0.57 ms** | **0.67 ms** |
| Average | **0.58 ms** | **0.73 ms** |
| 95th Percentile | **0.65 ms** | **0.89 ms** |
| Maximum | **2.78 ms** | **4.06 ms** |

For latency, lower values indicate faster event processing.

### Latency Comparison

![Latency Comparison](images/latency_comparison.jpeg)

**Figure 2: Comparison of minimum, average, 95th-percentile, and maximum latency.**

Proxmox VE recorded lower latency for every reported latency metric in the experiment.

---

## 7.3 Total Events Processed

The total number of benchmark events was:

| Hypervisor | Total Events |
|---|---:|
| Proxmox VE | **17,169** |
| VMware Workstation | **13,650** |

### Total Events Comparison

![Total Events Comparison](images/total_events_comparison.jpeg)

**Figure 3: Total Sysbench prime-calculation events completed during the benchmark.**

Proxmox VE processed **3,519 more events** than VMware Workstation during the recorded benchmark.

---

# 8. Performance Comparison

The main measured results are summarized below.

| Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Better Result |
|---|---:|---:|---|
| CPU Throughput | **1,716.69 eps** | 1,364.78 eps | **Proxmox VE** |
| Total Events | **17,169** | 13,650 | **Proxmox VE** |
| Minimum Latency | **0.57 ms** | 0.67 ms | **Proxmox VE** |
| Average Latency | **0.58 ms** | 0.73 ms | **Proxmox VE** |
| 95th Percentile | **0.65 ms** | 0.89 ms | **Proxmox VE** |
| Maximum Latency | **2.78 ms** | 4.06 ms | **Proxmox VE** |

---

# 9. Percentage Comparison

## 9.1 CPU Throughput

The recorded throughput values were:

```text
Proxmox VE      = 1716.69 eps
VMware          = 1364.78 eps
```

Difference:

```text
1716.69 - 1364.78 = 351.91 eps
```

Percentage advantage:

```text
(351.91 / 1364.78) × 100 ≈ 25.79%
```

Therefore:

> **Proxmox VE achieved approximately 25.79% higher CPU throughput than VMware Workstation in this experiment.**

---

## 9.2 Average Latency

The average latency values were:

```text
Proxmox VE      = 0.58 ms
VMware          = 0.73 ms
```

Difference:

```text
0.73 - 0.58 = 0.15 ms
```

Relative reduction compared with VMware:

```text
(0.15 / 0.73) × 100 ≈ 20.55%
```

Therefore:

> **Proxmox VE showed approximately 20.55% lower average latency than VMware Workstation.**

---

## 9.3 Maximum Latency

The maximum latency values were:

```text
Proxmox VE      = 2.78 ms
VMware          = 4.06 ms
```

Difference:

```text
4.06 - 2.78 = 1.28 ms
```

Relative reduction:

```text
(1.28 / 4.06) × 100 ≈ 31.53%
```

Therefore:

> **Proxmox VE recorded approximately 31.53% lower maximum latency.**

---

# 10. Technical Analysis

## 10.1 Type-1 Architecture

Proxmox VE is a bare-metal virtualization platform. It provides the virtualization layer directly on the physical machine and uses Linux/KVM virtualization technology.

The simplified execution path is:

```text
Physical Hardware
        ↓
Proxmox VE / KVM
        ↓
Ubuntu VM
        ↓
Sysbench
```

Because there is no general-purpose desktop operating system between the physical hardware and the virtualization layer, the architecture can provide efficient access to hardware resources.

---

## 10.2 Type-2 Architecture

VMware Workstation operates on top of a host operating system.

The simplified execution path is:

```text
Physical Hardware
        ↓
Host Operating System
        ↓
VMware Workstation
        ↓
Ubuntu VM
        ↓
Sysbench
```

The additional host OS layer can introduce additional scheduling and resource-management overhead.

---

## 10.3 CPU Scheduling

Virtual CPUs need to be scheduled onto physical CPU resources.

The host environment may also be running:

- Background processes
- System services
- Security software
- Desktop applications
- Operating-system tasks

These activities can affect when a virtual CPU gets physical CPU time.

This is particularly relevant when examining latency and latency spikes.

---

## 10.4 Latency Behavior

The experiment showed:

```text
Average latency:
Proxmox VE = 0.58 ms
VMware     = 0.73 ms
```

The maximum latency was:

```text
Proxmox VE = 2.78 ms
VMware     = 4.06 ms
```

The difference suggests that the Type-1 environment produced lower observed latency for this workload.

However, a single benchmark run does not prove that virtualization architecture is the only cause of the difference. Host configuration, CPU allocation, background processes, VM configuration, and other environmental factors can also influence benchmark results.

---

# 11. Discussion

The experimental results show a clear performance difference between the two tested environments.

### Observation 1 — Higher Throughput

Proxmox VE achieved:

```text
1716.69 events/sec
```

while VMware Workstation achieved:

```text
1364.78 events/sec
```

This gives Proxmox VE approximately a **25.79% throughput advantage** in the recorded experiment.

### Observation 2 — Lower Average Latency

Proxmox VE:

```text
0.58 ms
```

VMware Workstation:

```text
0.73 ms
```

The lower value indicates faster average event completion.

### Observation 3 — Lower Tail Latency

The 95th-percentile latency was:

```text
Proxmox VE      = 0.65 ms
VMware          = 0.89 ms
```

The maximum latency was:

```text
Proxmox VE      = 2.78 ms
VMware          = 4.06 ms
```

This indicates that the Proxmox result had lower observed latency even at the higher end of the distribution.

---

# 12. Advantages and Limitations

## Advantages of the Experiment

- Same benchmark workload was used.
- CPU throughput was directly measured.
- Multiple latency metrics were collected.
- Total benchmark events were recorded.
- The results were visualized using graphs.
- Type-1 and Type-2 architectures can be compared using measurable performance data.

## Limitations

The results should not be interpreted as a universal statement that every Type-1 hypervisor will always outperform every Type-2 hypervisor.

Performance can depend on:

- Physical CPU
- Number of assigned vCPUs
- RAM allocation
- Host OS
- Hypervisor configuration
- Background processes
- VM configuration
- CPU scheduling
- Storage configuration
- Number of benchmark repetitions

For stronger experimental validity, multiple benchmark runs should be performed and their averages and variation should be reported.

---

# 13. Conclusion

The Sysbench CPU benchmark demonstrated a measurable performance difference between the tested Type-1 and Type-2 virtualization environments.

The major findings were:

1. **Proxmox VE achieved 1,716.69 events/sec.**
2. **VMware Workstation achieved 1,364.78 events/sec.**
3. Proxmox VE achieved approximately **25.79% higher CPU throughput**.
4. Proxmox VE recorded lower average latency:
   - Proxmox VE: **0.58 ms**
   - VMware Workstation: **0.73 ms**
5. Proxmox VE recorded a lower 95th-percentile latency:
   - Proxmox VE: **0.65 ms**
   - VMware Workstation: **0.89 ms**
6. Proxmox VE recorded lower maximum latency:
   - Proxmox VE: **2.78 ms**
   - VMware Workstation: **4.06 ms**
7. Proxmox VE processed **3,519 more benchmark events**.

Based on the recorded benchmark, the **Type-1 Proxmox VE environment demonstrated better CPU throughput and lower latency than the tested Type-2 VMware Workstation environment**.

---

# 14. Applications

The results help demonstrate why virtualization architecture matters when selecting an environment for different workloads.

### Type-1 Hypervisors

Suitable for environments such as:

- Cloud infrastructure
- Data centers
- Enterprise servers
- Production virtualization
- High-performance workloads

Examples:

- Proxmox VE
- VMware ESXi
- Microsoft Hyper-V

### Type-2 Hypervisors

Useful for:

- Software development
- Testing
- Educational laboratories
- Desktop virtualization
- Running another operating system locally

Examples:

- VMware Workstation
- VirtualBox

---

# 15. Commands Used

```bash
# CPU information
lscpu

# Memory information
free -h

# Disk information
df -h

# Process monitoring
top

# Update packages
sudo apt update

# Install Sysbench
sudo apt install sysbench -y

# Check Sysbench version
sysbench --version

# Run CPU benchmark
sysbench cpu --cpu-max-prime=20000 run
```

---

# 16. Repository Structure

```text
Hypervisor-Performance-Analysis/
│
├── README.md
├── LAB_REPORT.md
│
└── images/
    ├── cpu_throughput_comparison.jpeg
    ├── latency_comparison.jpeg
    └── total_events_comparison.jpeg
```

---

# 17. Result Summary

```text
┌──────────────────────────────────────────────────────┐
│              FINAL PERFORMANCE SUMMARY               │
├──────────────────────┬────────────┬──────────────────┤
│ Metric               │ Proxmox VE │ VMware Workstation│
├──────────────────────┼────────────┼──────────────────┤
│ Type                  │ Type-1     │ Type-2           │
│ Throughput            │ 1716.69    │ 1364.78 eps      │
│ Total Events          │ 17169      │ 13650            │
│ Average Latency       │ 0.58 ms    │ 0.73 ms          │
│ 95th Percentile       │ 0.65 ms    │ 0.89 ms          │
│ Maximum Latency       │ 2.78 ms    │ 4.06 ms          │
└──────────────────────┴────────────┴──────────────────┘
```

---

## References

- Sysbench CPU benchmark
- Linux system monitoring utilities
- Proxmox VE virtualization platform
- VMware Workstation virtualization platform

---

**Laboratory Experiment — Cloud Computing / Computer Networks**
