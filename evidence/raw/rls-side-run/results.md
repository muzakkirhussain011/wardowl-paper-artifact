### Layout: random

| Selectivity | Readable | Backend | Strategy | Recall@10 | Complete | Examined | p50 ms | p95 ms | Leaks |
|---|---|---|---|---|---|---|---|---|---|
| 0.1% | 0.10% | exact | prefilter | 1.000 | 100% | 10 | 9.0 | 9.5 | 0 |
| 0.1% | 0.10% | exact | postfilter | 0.097 | 0% | 1000 | 47.0 | 50.2 | 0 |
| 0.1% | 0.10% | exact | naive top-k | 0.001 | 0% | 10 | 8.4 | 12.4 | 0 |
| 0.1% | 0.10% | exact | unprotected | 0.001 | 100% | 0 | 8.4 | 8.9 | 1998 |
| 0.1% | 0.10% | chroma | prefilter | 1.000 | 100% | 10 | 245.1 | 263.0 | 0 |
| 0.1% | 0.10% | chroma | postfilter | 0.096 | 0% | 1000 | 223.3 | 278.7 | 0 |
| 0.1% | 0.10% | chroma | naive top-k | 0.001 | 0% | 10 | 16.0 | 17.6 | 0 |
| 0.1% | 0.10% | pgvector | prefilter | 1.000 | 100% | 10 | 3.4 | 4.1 | 0 |
| 0.1% | 0.10% | pgvector | postfilter | 0.096 | 0% | 1000 | 99.9 | 125.1 | 0 |
| 0.1% | 0.10% | pgvector | naive top-k | 0.001 | 0% | 10 | 4.2 | 5.8 | 0 |
| 0.1% | 0.10% | pgvector, no iterative scan | prefilter | 1.000 | 100% | 10 | 2.9 | 3.5 | 0 |
| 0.1% | 0.10% | pgvector | row-level security | 1.000 | 100% | n/a | 3.0 | 3.6 | 0 |
| 1.0% | 1.00% | exact | prefilter | 1.000 | 100% | 10 | 8.4 | 8.8 | 0 |
| 1.0% | 1.00% | exact | postfilter | 0.858 | 52% | 960.4 | 45.8 | 49.1 | 0 |
| 1.0% | 1.00% | exact | naive top-k | 0.010 | 0% | 10 | 8.4 | 8.9 | 0 |
| 1.0% | 1.00% | exact | unprotected | 0.010 | 100% | 0 | 8.4 | 10.7 | 1980 |
| 1.0% | 1.00% | chroma | prefilter | 1.000 | 100% | 10 | 210.0 | 218.6 | 0 |
| 1.0% | 1.00% | chroma | postfilter | 0.853 | 54% | 955 | 220.8 | 274.0 | 0 |
| 1.0% | 1.00% | chroma | naive top-k | 0.010 | 0% | 10 | 16.1 | 20.2 | 0 |
| 1.0% | 1.00% | pgvector | prefilter | 1.000 | 100% | 10 | 10.2 | 11.9 | 0 |
| 1.0% | 1.00% | pgvector | postfilter | 0.850 | 52% | 953.2 | 98.7 | 125.9 | 0 |
| 1.0% | 1.00% | pgvector | naive top-k | 0.010 | 0% | 10 | 4.3 | 5.8 | 0 |
| 1.0% | 1.00% | pgvector, no iterative scan | prefilter | 1.000 | 100% | 10 | 10.6 | 12.1 | 0 |
| 1.0% | 1.00% | pgvector | row-level security | 1.000 | 100% | n/a | 9.9 | 12.0 | 0 |
| 5.0% | 5.01% | exact | prefilter | 1.000 | 100% | 10 | 8.9 | 11.5 | 0 |
| 5.0% | 5.01% | exact | postfilter | 1.000 | 100% | 491.2 | 32.8 | 34.5 | 0 |
| 5.0% | 5.01% | exact | naive top-k | 0.047 | 0% | 10 | 8.7 | 9.1 | 0 |
| 5.0% | 5.01% | exact | unprotected | 0.047 | 100% | 0 | 8.4 | 11.8 | 1906 |
| 5.0% | 5.01% | chroma | prefilter | 0.999 | 100% | 10 | 412.8 | 434.7 | 0 |
| 5.0% | 5.01% | chroma | postfilter | 0.986 | 100% | 496 | 116.2 | 140.1 | 0 |
| 5.0% | 5.01% | chroma | naive top-k | 0.046 | 0% | 10 | 15.8 | 17.3 | 0 |
| 5.0% | 5.01% | pgvector | prefilter | 0.974 | 100% | 10 | 12.2 | 20.6 | 0 |
| 5.0% | 5.01% | pgvector | postfilter | 0.991 | 100% | 491.2 | 51.8 | 69.2 | 0 |
| 5.0% | 5.01% | pgvector | naive top-k | 0.045 | 0% | 10 | 4.3 | 5.7 | 0 |
| 5.0% | 5.01% | pgvector, no iterative scan | prefilter | 0.197 | 100% | 2 | 4.5 | 6.3 | 0 |
| 5.0% | 5.01% | pgvector | row-level security | 1.000 | 100% | n/a | 38.9 | 42.5 | 0 |
| 20.0% | 20.00% | exact | prefilter | 1.000 | 100% | 10 | 9.0 | 9.7 | 0 |
| 20.0% | 20.00% | exact | postfilter | 1.000 | 100% | 128.2 | 19.1 | 20.0 | 0 |
| 20.0% | 20.00% | exact | naive top-k | 0.193 | 0% | 10 | 8.8 | 9.2 | 0 |
| 20.0% | 20.00% | exact | unprotected | 0.193 | 100% | 0 | 8.4 | 8.9 | 1614 |
| 20.0% | 20.00% | chroma | prefilter | 0.997 | 100% | 10 | 287.7 | 310.0 | 0 |
| 20.0% | 20.00% | chroma | postfilter | 0.978 | 100% | 127 | 47.8 | 55.9 | 0 |
| 20.0% | 20.00% | chroma | naive top-k | 0.194 | 0% | 10 | 16.2 | 17.5 | 0 |
| 20.0% | 20.00% | pgvector | prefilter | 0.965 | 100% | 10 | 6.5 | 10.0 | 0 |
| 20.0% | 20.00% | pgvector | postfilter | 0.979 | 100% | 128.8 | 15.7 | 20.8 | 0 |
| 20.0% | 20.00% | pgvector | naive top-k | 0.193 | 0% | 10 | 4.1 | 5.7 | 0 |
| 20.0% | 20.00% | pgvector, no iterative scan | prefilter | 0.764 | 100% | 7.8 | 4.5 | 6.0 | 0 |
| 20.0% | 20.00% | pgvector | row-level security | 0.998 | 100% | n/a | 153.6 | 161.7 | 0 |
| 100.0% | 100.00% | exact | prefilter | 1.000 | 100% | 10 | 8.9 | 9.3 | 0 |
| 100.0% | 100.00% | exact | postfilter | 1.000 | 100% | 40 | 8.8 | 12.2 | 0 |
| 100.0% | 100.00% | exact | naive top-k | 1.000 | 100% | 10 | 8.4 | 8.9 | 0 |
| 100.0% | 100.00% | exact | unprotected | 1.000 | 100% | 0 | 8.4 | 8.7 | 0 |
| 100.0% | 100.00% | chroma | prefilter | 0.987 | 100% | 10 | 841.0 | 904.2 | 0 |
| 100.0% | 100.00% | chroma | postfilter | 0.987 | 100% | 40 | 18.7 | 20.6 | 0 |
| 100.0% | 100.00% | chroma | naive top-k | 0.987 | 100% | 10 | 15.9 | 17.1 | 0 |
| 100.0% | 100.00% | pgvector | prefilter | 0.979 | 100% | 10 | 5.3 | 7.0 | 0 |
| 100.0% | 100.00% | pgvector | postfilter | 0.979 | 100% | 40 | 5.2 | 6.6 | 0 |
| 100.0% | 100.00% | pgvector | naive top-k | 0.979 | 100% | 10 | 4.1 | 5.6 | 0 |
| 100.0% | 100.00% | pgvector, no iterative scan | prefilter | 0.979 | 100% | 10 | 4.8 | 6.5 | 0 |
| 100.0% | 100.00% | pgvector | row-level security | 0.998 | 100% | n/a | 545.4 | 570.1 | 0 |

### Layout: aligned

| Selectivity | Readable | Backend | Strategy | Recall@10 | Complete | Examined | p50 ms | p95 ms | Leaks |
|---|---|---|---|---|---|---|---|---|---|
| 0.1% | 0.14% | exact | prefilter | 1.000 | 100% | 10 | 8.7 | 9.2 | 0 |
| 0.1% | 0.14% | exact | postfilter | 0.972 | 91% | 290.8 | 18.4 | 45.9 | 0 |
| 0.1% | 0.14% | exact | naive top-k | 0.289 | 4% | 10 | 8.4 | 9.2 | 0 |
| 0.1% | 0.14% | exact | unprotected | 0.289 | 100% | 0 | 8.3 | 8.8 | 1424 |
| 0.1% | 0.14% | chroma | prefilter | 0.999 | 100% | 10 | 240.3 | 246.3 | 0 |
| 0.1% | 0.14% | chroma | postfilter | 0.967 | 92% | 287.8 | 48.0 | 233.2 | 0 |
| 0.1% | 0.14% | chroma | naive top-k | 0.290 | 4% | 10 | 15.6 | 16.8 | 0 |
| 0.1% | 0.14% | pgvector | prefilter | 0.999 | 100% | 10 | 3.2 | 4.8 | 0 |
| 0.1% | 0.14% | pgvector | postfilter | 0.969 | 92% | 289.6 | 16.8 | 112.5 | 0 |
| 0.1% | 0.14% | pgvector | naive top-k | 0.290 | 4% | 10 | 4.1 | 5.5 | 0 |
| 0.1% | 0.14% | pgvector, no iterative scan | prefilter | 0.999 | 100% | 10 | 2.8 | 4.3 | 0 |
| 0.1% | 0.14% | pgvector | row-level security | 0.999 | 99% | n/a | 2.9 | 4.3 | 0 |
| 1.0% | 1.08% | exact | prefilter | 1.000 | 100% | 10 | 8.5 | 11.4 | 0 |
| 1.0% | 1.08% | exact | postfilter | 0.992 | 98% | 244.6 | 18.3 | 32.9 | 0 |
| 1.0% | 1.08% | exact | naive top-k | 0.295 | 4% | 10 | 8.4 | 9.3 | 0 |
| 1.0% | 1.08% | exact | unprotected | 0.295 | 100% | 0 | 8.4 | 8.9 | 1409 |
| 1.0% | 1.08% | chroma | prefilter | 0.999 | 100% | 10 | 198.3 | 221.8 | 0 |
| 1.0% | 1.08% | chroma | postfilter | 0.986 | 97% | 241 | 47.6 | 144.1 | 0 |
| 1.0% | 1.08% | chroma | naive top-k | 0.296 | 4% | 10 | 15.7 | 17.0 | 0 |
| 1.0% | 1.08% | pgvector | prefilter | 0.999 | 100% | 10 | 10.2 | 16.7 | 0 |
| 1.0% | 1.08% | pgvector | postfilter | 0.985 | 97% | 242.8 | 16.4 | 74.8 | 0 |
| 1.0% | 1.08% | pgvector | naive top-k | 0.296 | 4% | 10 | 3.9 | 5.3 | 0 |
| 1.0% | 1.08% | pgvector, no iterative scan | prefilter | 0.970 | 100% | 9.7 | 9.3 | 14.0 | 0 |
| 1.0% | 1.08% | pgvector | row-level security | 0.999 | 100% | n/a | 9.0 | 13.0 | 0 |
| 5.0% | 5.21% | exact | prefilter | 1.000 | 100% | 10 | 8.5 | 9.0 | 0 |
| 5.0% | 5.21% | exact | postfilter | 1.000 | 100% | 50.2 | 8.8 | 18.4 | 0 |
| 5.0% | 5.21% | exact | naive top-k | 0.641 | 12% | 10 | 8.4 | 8.9 | 0 |
| 5.0% | 5.21% | exact | unprotected | 0.641 | 100% | 0 | 8.2 | 8.7 | 717 |
| 5.0% | 5.21% | chroma | prefilter | 0.999 | 100% | 10 | 398.8 | 424.0 | 0 |
| 5.0% | 5.21% | chroma | postfilter | 0.989 | 100% | 49.6 | 18.0 | 47.1 | 0 |
| 5.0% | 5.21% | chroma | naive top-k | 0.641 | 12% | 10 | 15.8 | 16.9 | 0 |
| 5.0% | 5.21% | pgvector | prefilter | 0.977 | 100% | 10 | 5.7 | 47.6 | 0 |
| 5.0% | 5.21% | pgvector | postfilter | 0.977 | 100% | 49 | 5.0 | 17.8 | 0 |
| 5.0% | 5.21% | pgvector | naive top-k | 0.647 | 13% | 10 | 3.9 | 5.1 | 0 |
| 5.0% | 5.21% | pgvector, no iterative scan | prefilter | 0.963 | 100% | 9.8 | 5.5 | 47.5 | 0 |
| 5.0% | 5.21% | pgvector | row-level security | 0.999 | 100% | n/a | 38.6 | 47.3 | 0 |
| 20.0% | 20.36% | exact | prefilter | 1.000 | 100% | 10 | 8.9 | 12.2 | 0 |
| 20.0% | 20.36% | exact | postfilter | 1.000 | 100% | 48.4 | 8.8 | 18.3 | 0 |
| 20.0% | 20.36% | exact | naive top-k | 0.548 | 7% | 10 | 8.4 | 8.8 | 0 |
| 20.0% | 20.36% | exact | unprotected | 0.548 | 100% | 0 | 8.3 | 8.9 | 903 |
| 20.0% | 20.36% | chroma | prefilter | 0.998 | 100% | 10 | 280.0 | 300.2 | 0 |
| 20.0% | 20.36% | chroma | postfilter | 0.988 | 100% | 48.4 | 18.6 | 46.6 | 0 |
| 20.0% | 20.36% | chroma | naive top-k | 0.550 | 7% | 10 | 15.7 | 17.1 | 0 |
| 20.0% | 20.36% | pgvector | prefilter | 0.971 | 100% | 10 | 4.7 | 7.5 | 0 |
| 20.0% | 20.36% | pgvector | postfilter | 0.976 | 100% | 50.2 | 5.1 | 16.2 | 0 |
| 20.0% | 20.36% | pgvector | naive top-k | 0.552 | 8% | 10 | 4.2 | 5.6 | 0 |
| 20.0% | 20.36% | pgvector, no iterative scan | prefilter | 0.949 | 100% | 9.7 | 4.4 | 5.7 | 0 |
| 20.0% | 20.36% | pgvector | row-level security | 0.998 | 100% | n/a | 155.2 | 166.2 | 0 |
| 100.0% | 100.00% | exact | prefilter | 1.000 | 100% | 10 | 8.8 | 9.4 | 0 |
| 100.0% | 100.00% | exact | postfilter | 1.000 | 100% | 40 | 8.8 | 9.7 | 0 |
| 100.0% | 100.00% | exact | naive top-k | 1.000 | 100% | 10 | 8.4 | 9.9 | 0 |
| 100.0% | 100.00% | exact | unprotected | 1.000 | 100% | 0 | 8.3 | 8.8 | 0 |
| 100.0% | 100.00% | chroma | prefilter | 0.987 | 100% | 10 | 869.6 | 924.0 | 0 |
| 100.0% | 100.00% | chroma | postfilter | 0.987 | 100% | 40 | 18.4 | 20.4 | 0 |
| 100.0% | 100.00% | chroma | naive top-k | 0.987 | 100% | 10 | 16.2 | 18.1 | 0 |
| 100.0% | 100.00% | pgvector | prefilter | 0.979 | 100% | 10 | 5.1 | 6.8 | 0 |
| 100.0% | 100.00% | pgvector | postfilter | 0.979 | 100% | 40 | 5.1 | 6.5 | 0 |
| 100.0% | 100.00% | pgvector | naive top-k | 0.979 | 100% | 10 | 4.0 | 5.4 | 0 |
| 100.0% | 100.00% | pgvector, no iterative scan | prefilter | 0.979 | 100% | 10 | 4.6 | 6.2 | 0 |
| 100.0% | 100.00% | pgvector | row-level security | 0.998 | 100% | n/a | 549.9 | 576.9 | 0 |

### Layout: misaligned

| Selectivity | Readable | Backend | Strategy | Recall@10 | Complete | Examined | p50 ms | p95 ms | Leaks |
|---|---|---|---|---|---|---|---|---|---|
| 0.1% | 0.06% | exact | prefilter | 1.000 | 100% | 9.7 | 8.5 | 9.0 | 0 |
| 0.1% | 0.06% | exact | postfilter | 0.000 | 0% | 1000 | 46.3 | 50.0 | 0 |
| 0.1% | 0.06% | exact | naive top-k | 0.000 | 0% | 10 | 8.5 | 9.0 | 0 |
| 0.1% | 0.06% | exact | unprotected | 0.000 | 100% | 0 | 8.3 | 8.9 | 2000 |
| 0.1% | 0.06% | chroma | prefilter | 1.000 | 100% | 9.7 | 241.4 | 250.1 | 0 |
| 0.1% | 0.06% | chroma | postfilter | 0.000 | 0% | 1000 | 219.0 | 271.5 | 0 |
| 0.1% | 0.06% | chroma | naive top-k | 0.000 | 0% | 10 | 16.1 | 17.2 | 0 |
| 0.1% | 0.06% | pgvector | prefilter | 1.000 | 100% | 9.7 | 2.6 | 3.8 | 0 |
| 0.1% | 0.06% | pgvector | postfilter | 0.000 | 0% | 1000 | 98.2 | 120.3 | 0 |
| 0.1% | 0.06% | pgvector | naive top-k | 0.000 | 0% | 10 | 4.4 | 5.7 | 0 |
| 0.1% | 0.06% | pgvector, no iterative scan | prefilter | 1.000 | 100% | 9.7 | 2.5 | 3.6 | 0 |
| 0.1% | 0.06% | pgvector | row-level security | 1.000 | 92% | n/a | 1.9 | 3.0 | 0 |
| 1.0% | 0.92% | exact | prefilter | 1.000 | 100% | 10 | 8.7 | 9.2 | 0 |
| 1.0% | 0.92% | exact | postfilter | 0.049 | 0% | 1000 | 47.1 | 49.9 | 0 |
| 1.0% | 0.92% | exact | naive top-k | 0.000 | 0% | 10 | 8.4 | 12.1 | 0 |
| 1.0% | 0.92% | exact | unprotected | 0.000 | 100% | 0 | 8.3 | 9.0 | 2000 |
| 1.0% | 0.92% | chroma | prefilter | 0.999 | 100% | 10 | 229.4 | 243.4 | 0 |
| 1.0% | 0.92% | chroma | postfilter | 0.046 | 0% | 1000 | 221.0 | 275.2 | 0 |
| 1.0% | 0.92% | chroma | naive top-k | 0.000 | 0% | 10 | 15.7 | 17.0 | 0 |
| 1.0% | 0.92% | pgvector | prefilter | 0.984 | 100% | 10 | 9.9 | 133.3 | 0 |
| 1.0% | 0.92% | pgvector | postfilter | 0.047 | 0% | 1000 | 97.3 | 117.8 | 0 |
| 1.0% | 0.92% | pgvector | naive top-k | 0.000 | 0% | 10 | 4.3 | 5.8 | 0 |
| 1.0% | 0.92% | pgvector, no iterative scan | prefilter | 0.914 | 100% | 9.2 | 7.5 | 12.5 | 0 |
| 1.0% | 0.92% | pgvector | row-level security | 0.999 | 100% | n/a | 7.7 | 12.6 | 0 |
| 5.0% | 4.78% | exact | prefilter | 1.000 | 100% | 10 | 8.6 | 9.0 | 0 |
| 5.0% | 4.78% | exact | postfilter | 0.325 | 10% | 991 | 46.3 | 48.6 | 0 |
| 5.0% | 4.78% | exact | naive top-k | 0.000 | 0% | 10 | 8.4 | 9.1 | 0 |
| 5.0% | 4.78% | exact | unprotected | 0.000 | 100% | 0 | 8.3 | 10.5 | 2000 |
| 5.0% | 4.78% | chroma | prefilter | 0.995 | 100% | 10 | 426.7 | 444.0 | 0 |
| 5.0% | 4.78% | chroma | postfilter | 0.308 | 8% | 996.4 | 217.5 | 270.7 | 0 |
| 5.0% | 4.78% | chroma | naive top-k | 0.000 | 0% | 10 | 15.9 | 17.0 | 0 |
| 5.0% | 4.78% | pgvector | prefilter | 0.950 | 100% | 10 | 83.1 | 134.8 | 0 |
| 5.0% | 4.78% | pgvector | postfilter | 0.313 | 10% | 992.8 | 96.8 | 119.0 | 0 |
| 5.0% | 4.78% | pgvector | naive top-k | 0.000 | 0% | 10 | 4.1 | 5.7 | 0 |
| 5.0% | 4.78% | pgvector, no iterative scan | prefilter | 0.113 | 100% | 1.1 | 5.0 | 43.0 | 0 |
| 5.0% | 4.78% | pgvector | row-level security | 1.000 | 100% | n/a | 32.1 | 42.5 | 0 |
| 20.0% | 19.89% | exact | prefilter | 1.000 | 100% | 10 | 8.8 | 9.2 | 0 |
| 20.0% | 19.89% | exact | postfilter | 1.000 | 100% | 365.8 | 19.9 | 34.4 | 0 |
| 20.0% | 19.89% | exact | naive top-k | 0.041 | 0% | 10 | 8.3 | 8.7 | 0 |
| 20.0% | 19.89% | exact | unprotected | 0.041 | 100% | 0 | 8.3 | 8.9 | 1918 |
| 20.0% | 19.89% | chroma | prefilter | 0.997 | 100% | 10 | 285.8 | 308.6 | 0 |
| 20.0% | 19.89% | chroma | postfilter | 0.969 | 100% | 371.2 | 56.3 | 142.9 | 0 |
| 20.0% | 19.89% | chroma | naive top-k | 0.041 | 0% | 10 | 16.1 | 17.6 | 0 |
| 20.0% | 19.89% | pgvector | prefilter | 0.950 | 100% | 10 | 10.9 | 17.6 | 0 |
| 20.0% | 19.89% | pgvector | postfilter | 0.974 | 100% | 371.8 | 22.0 | 63.4 | 0 |
| 20.0% | 19.89% | pgvector | naive top-k | 0.040 | 0% | 10 | 4.4 | 5.8 | 0 |
| 20.0% | 19.89% | pgvector, no iterative scan | prefilter | 0.220 | 100% | 2.2 | 4.2 | 5.6 | 0 |
| 20.0% | 19.89% | pgvector | row-level security | 0.998 | 100% | n/a | 160.5 | 179.2 | 0 |
| 100.0% | 100.00% | exact | prefilter | 1.000 | 100% | 10 | 9.3 | 10.1 | 0 |
| 100.0% | 100.00% | exact | postfilter | 1.000 | 100% | 40 | 9.2 | 13.0 | 0 |
| 100.0% | 100.00% | exact | naive top-k | 1.000 | 100% | 10 | 8.7 | 9.3 | 0 |
| 100.0% | 100.00% | exact | unprotected | 1.000 | 100% | 0 | 8.4 | 8.9 | 0 |
| 100.0% | 100.00% | chroma | prefilter | 0.987 | 100% | 10 | 868.7 | 935.0 | 0 |
| 100.0% | 100.00% | chroma | postfilter | 0.987 | 100% | 40 | 19.0 | 21.6 | 0 |
| 100.0% | 100.00% | chroma | naive top-k | 0.987 | 100% | 10 | 15.9 | 17.2 | 0 |
| 100.0% | 100.00% | pgvector | prefilter | 0.979 | 100% | 10 | 5.2 | 6.9 | 0 |
| 100.0% | 100.00% | pgvector | postfilter | 0.979 | 100% | 40 | 5.0 | 6.3 | 0 |
| 100.0% | 100.00% | pgvector | naive top-k | 0.979 | 100% | 10 | 4.2 | 5.6 | 0 |
| 100.0% | 100.00% | pgvector, no iterative scan | prefilter | 0.979 | 100% | 10 | 4.9 | 6.8 | 0 |
| 100.0% | 100.00% | pgvector | row-level security | 0.998 | 100% | n/a | 556.1 | 580.5 | 0 |
