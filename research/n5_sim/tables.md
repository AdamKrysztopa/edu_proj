# N5 simulation tables (SYNTHETIC — not evidence about learners or experts)

Spec sha256 `85da9dbe4c1fd1d5400857bda2a5c9c091ebe387bd69aacdcfccc6c2e2685937`.

Pass = share of replicates with |f0 − ref| ≤ τ·ref; failures count as misses. Achievable = pass ≥ 0.80 (our choice). Forms: s22 = raw gold-uncaught (as written); lp = Lincoln–Petersen unseen; w_true = unseen written items (truth); w_obs = Lincoln–Petersen on gold items the corpus audit finds written.

## default grid: cells where some estimator (chao1, jackknife, mh) is achievable, by form and ρ

| ρ | cells | s22 τ=0.1 | s22 τ=0.25 | s22 τ=0.5 | lp τ=0.1 | lp τ=0.25 | lp τ=0.5 | w_true τ=0.1 | w_true τ=0.25 | w_true τ=0.5 | w_obs τ=0.1 | w_obs τ=0.25 | w_obs τ=0.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | 108 | 0 | 0 | 21 | 0 | 0 | 14 | 0 | 0 | 28 | 0 | 0 | 25 |
| 0.3 | 108 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0.6 | 108 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## default grid: stop-condition readings at ρ = 0, low heterogeneity, τ = 0.5

Best estimator pass and the singleton stand-in, per form (ds4: g_W 0.9, g_Z/g_W 1, no false non-matches).

| cell | s22 best | s22 f1 | lp best | lp f1 | w_true best | w_true f1 | w_obs best | w_obs f1 |
|---|---|---|---|---|---|---|---|---|
| N50_nw0.0_k2_low_rho0.0_g1.0 | 0.54 mh | 0.92 | 0.54 mh | 0.92 | 0.54 mh | 0.92 | 0.54 mh | 0.92 |
| N50_nw0.0_k2_low_rho0.0_g0.6 | 0.82 jackknife | 0.63 | 0.55 mh | 0.84 | 0.58 mh | 0.92 | 0.55 mh | 0.84 |
| N50_nw0.0_k3_low_rho0.0_g1.0 | 0.89 jackknife | 0.76 | 0.89 jackknife | 0.76 | 0.89 jackknife | 0.76 | 0.89 jackknife | 0.76 |
| N50_nw0.0_k3_low_rho0.0_g0.6 | 0.56 jackknife | 0.24 | 0.81 jackknife | 0.64 | 0.88 jackknife | 0.74 | 0.81 jackknife | 0.64 |
| N50_nw0.0_k5_low_rho0.0_g1.0 | 0.61 mh | 0.29 | 0.61 mh | 0.29 | 0.61 mh | 0.29 | 0.61 mh | 0.29 |
| N50_nw0.0_k5_low_rho0.0_g0.6 | 0.40 chao1 | 0.05 | 0.54 mh | 0.29 | 0.60 mh | 0.30 | 0.54 mh | 0.29 |
| N50_nw0.2_k2_low_rho0.0_g1.0 | 0.51 chao1 | 0.65 | 0.51 chao1 | 0.65 | 0.51 chao1 | 0.91 | 0.51 chao1 | 0.91 |
| N50_nw0.2_k2_low_rho0.0_g0.6 | 0.52 mh | 0.89 | 0.47 mh | 0.65 | 0.51 mh | 0.89 | 0.50 mh | 0.81 |
| N50_nw0.2_k3_low_rho0.0_g1.0 | 0.51 mh | 0.87 | 0.51 mh | 0.87 | 0.85 jackknife | 0.73 | 0.85 jackknife | 0.73 |
| N50_nw0.2_k3_low_rho0.0_g0.6 | 0.86 jackknife | 0.75 | 0.49 mh | 0.81 | 0.84 jackknife | 0.71 | 0.75 jackknife | 0.63 |
| N50_nw0.2_k5_low_rho0.0_g1.0 | 0.81 jackknife | 0.94 | 0.81 jackknife | 0.94 | 0.57 mh | 0.30 | 0.57 mh | 0.30 |
| N50_nw0.2_k5_low_rho0.0_g0.6 | 0.79 jackknife | 0.63 | 0.74 jackknife | 0.83 | 0.57 mh | 0.28 | 0.51 mh | 0.31 |
| N50_nw0.5_k2_low_rho0.0_g1.0 | 0.33 chao1 | 0.00 | 0.33 chao1 | 0.00 | 0.44 chao1 | 0.85 | 0.44 chao1 | 0.85 |
| N50_nw0.5_k2_low_rho0.0_g0.6 | 0.41 chao1 | 0.47 | 0.29 chao1 | 0.05 | 0.48 chao1 | 0.83 | 0.45 chao1 | 0.70 |
| N50_nw0.5_k3_low_rho0.0_g1.0 | 0.17 mh | 0.04 | 0.17 mh | 0.04 | 0.77 jackknife | 0.67 | 0.77 jackknife | 0.67 |
| N50_nw0.5_k3_low_rho0.0_g0.6 | 0.38 mh | 0.58 | 0.19 mh | 0.10 | 0.77 jackknife | 0.69 | 0.65 jackknife | 0.56 |
| N50_nw0.5_k5_low_rho0.0_g1.0 | 0.05 chao1 | 0.02 | 0.05 chao1 | 0.02 | 0.49 jackknife | 0.37 | 0.49 jackknife | 0.37 |
| N50_nw0.5_k5_low_rho0.0_g0.6 | 0.22 jackknife | 0.52 | 0.05 chao1 | 0.06 | 0.45 mh | 0.34 | 0.40 mh | 0.30 |
| N200_nw0.0_k2_low_rho0.0_g1.0 | 0.84 mh | 1.00 | 0.84 mh | 1.00 | 0.84 mh | 1.00 | 0.84 mh | 1.00 |
| N200_nw0.0_k2_low_rho0.0_g0.6 | 0.98 jackknife | 0.66 | 0.88 mh | 0.99 | 0.87 mh | 1.00 | 0.88 mh | 0.99 |
| N200_nw0.0_k3_low_rho0.0_g1.0 | 1.00 jackknife | 0.88 | 1.00 jackknife | 0.88 | 1.00 jackknife | 0.88 | 1.00 jackknife | 0.88 |
| N200_nw0.0_k3_low_rho0.0_g0.6 | 0.73 jackknife | 0.05 | 0.98 jackknife | 0.86 | 1.00 jackknife | 0.90 | 0.98 jackknife | 0.86 |
| N200_nw0.0_k5_low_rho0.0_g1.0 | 0.90 mh | 0.11 | 0.90 mh | 0.11 | 0.90 mh | 0.11 | 0.90 mh | 0.11 |
| N200_nw0.0_k5_low_rho0.0_g0.6 | 0.44 chao1 | 0.00 | 0.90 chao1 | 0.12 | 0.94 chao1 | 0.10 | 0.90 chao1 | 0.12 |
| N200_nw0.2_k2_low_rho0.0_g1.0 | 0.67 mh | 0.76 | 0.67 mh | 0.76 | 0.84 mh | 1.00 | 0.84 mh | 1.00 |
| N200_nw0.2_k2_low_rho0.0_g0.6 | 0.83 mh | 1.00 | 0.71 mh | 0.72 | 0.83 mh | 1.00 | 0.82 mh | 0.99 |
| N200_nw0.2_k3_low_rho0.0_g1.0 | 0.61 mh | 0.99 | 0.61 mh | 0.99 | 0.99 jackknife | 0.86 | 0.99 jackknife | 0.86 |
| N200_nw0.2_k3_low_rho0.0_g0.6 | 1.00 jackknife | 0.92 | 0.64 mh | 0.98 | 0.99 jackknife | 0.87 | 0.98 jackknife | 0.80 |
| N200_nw0.2_k5_low_rho0.0_g1.0 | 0.95 jackknife | 1.00 | 0.95 jackknife | 1.00 | 0.87 mh | 0.14 | 0.87 mh | 0.14 |
| N200_nw0.2_k5_low_rho0.0_g0.6 | 0.97 jackknife | 0.72 | 0.92 jackknife | 1.00 | 0.86 mh | 0.13 | 0.82 mh | 0.19 |
| N200_nw0.5_k2_low_rho0.0_g1.0 | 0.14 mh | 0.00 | 0.14 mh | 0.00 | 0.73 mh | 0.99 | 0.73 mh | 0.99 |
| N200_nw0.5_k2_low_rho0.0_g0.6 | 0.52 mh | 0.32 | 0.15 mh | 0.00 | 0.76 mh | 0.98 | 0.74 mh | 0.95 |
| N200_nw0.5_k3_low_rho0.0_g1.0 | 0.05 mh | 0.00 | 0.05 mh | 0.00 | 0.97 jackknife | 0.83 | 0.97 jackknife | 0.83 |
| N200_nw0.5_k3_low_rho0.0_g0.6 | 0.34 mh | 0.65 | 0.04 mh | 0.00 | 0.98 jackknife | 0.81 | 0.95 jackknife | 0.76 |
| N200_nw0.5_k5_low_rho0.0_g1.0 | 0.00 mh | 0.00 | 0.00 mh | 0.00 | 0.76 mh | 0.21 | 0.76 mh | 0.21 |
| N200_nw0.5_k5_low_rho0.0_g0.6 | 0.06 jackknife | 0.47 | 0.00 mh | 0.00 | 0.79 mh | 0.18 | 0.73 mh | 0.23 |

## ds4 grid: cells where some estimator (chao1, jackknife, mh) is achievable, by form and ρ

| ρ | cells | s22 τ=0.1 | s22 τ=0.25 | s22 τ=0.5 | lp τ=0.1 | lp τ=0.25 | lp τ=0.5 | w_true τ=0.1 | w_true τ=0.25 | w_true τ=0.5 | w_obs τ=0.1 | w_obs τ=0.25 | w_obs τ=0.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | 1728 | 0 | 38 | 325 | 0 | 0 | 146 | 0 | 0 | 387 | 0 | 0 | 278 |
| 0.3 | 1728 | 0 | 5 | 136 | 0 | 0 | 32 | 0 | 0 | 181 | 0 | 0 | 88 |
| 0.6 | 1728 | 0 | 0 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## ds4 grid: stop-condition readings at ρ = 0, low heterogeneity, τ = 0.5

Best estimator pass and the singleton stand-in, per form (ds4: g_W 0.9, g_Z/g_W 1, no false non-matches).

| cell | s22 best | s22 f1 | lp best | lp f1 | w_true best | w_true f1 | w_obs best | w_obs f1 |
|---|---|---|---|---|---|---|---|---|
| N50_nw0.0_k2_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.54 chao1 | 0.19 | 0.51 chao1 | 0.12 | 0.56 chao1 | 0.10 | 0.51 chao1 | 0.12 |
| N50_nw0.0_k2_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.50 chao1 | 0.21 | 0.48 chao1 | 0.14 | 0.54 chao1 | 0.13 | 0.48 chao1 | 0.14 |
| N50_nw0.0_k2_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.82 jackknife | 0.62 | 0.72 jackknife | 0.73 | 0.76 jackknife | 0.75 | 0.72 jackknife | 0.73 |
| N50_nw0.0_k2_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.84 jackknife | 0.60 | 0.73 jackknife | 0.71 | 0.76 jackknife | 0.72 | 0.73 jackknife | 0.71 |
| N50_nw0.0_k3_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.51 chao1 | 0.62 | 0.51 mh | 0.47 | 0.51 chao1 | 0.48 | 0.51 mh | 0.47 |
| N50_nw0.0_k3_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.50 chao1 | 0.64 | 0.49 mh | 0.51 | 0.52 chao1 | 0.50 | 0.49 mh | 0.51 |
| N50_nw0.0_k3_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.70 jackknife | 0.28 | 0.77 jackknife | 0.39 | 0.80 jackknife | 0.38 | 0.77 jackknife | 0.39 |
| N50_nw0.0_k3_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.64 jackknife | 0.28 | 0.72 jackknife | 0.35 | 0.74 jackknife | 0.37 | 0.72 jackknife | 0.35 |
| N50_nw0.0_k5_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.82 jackknife | 0.90 | 0.75 jackknife | 0.88 | 0.75 jackknife | 0.87 | 0.75 jackknife | 0.88 |
| N50_nw0.0_k5_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.84 jackknife | 0.89 | 0.76 jackknife | 0.88 | 0.75 jackknife | 0.88 | 0.76 jackknife | 0.88 |
| N50_nw0.0_k5_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.51 mh | 0.13 | 0.50 mh | 0.17 | 0.54 mh | 0.18 | 0.50 mh | 0.17 |
| N50_nw0.0_k5_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.47 mh | 0.11 | 0.48 mh | 0.14 | 0.50 mh | 0.16 | 0.48 mh | 0.14 |
| N50_nw0.2_k2_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.51 chao1 | 0.03 | 0.49 chao1 | 0.01 | 0.51 chao1 | 0.16 | 0.49 chao1 | 0.16 |
| N50_nw0.2_k2_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.47 chao1 | 0.03 | 0.44 mh | 0.02 | 0.51 chao1 | 0.14 | 0.50 chao1 | 0.15 |
| N50_nw0.2_k2_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.53 mh | 0.93 | 0.47 mh | 0.86 | 0.73 jackknife | 0.72 | 0.69 jackknife | 0.69 |
| N50_nw0.2_k2_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.50 mh | 0.95 | 0.45 mh | 0.91 | 0.75 jackknife | 0.73 | 0.71 jackknife | 0.70 |
| N50_nw0.2_k3_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.45 chao1 | 0.23 | 0.43 chao1 | 0.14 | 0.46 chao1 | 0.46 | 0.44 chao1 | 0.46 |
| N50_nw0.2_k3_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.45 chao1 | 0.21 | 0.45 chao1 | 0.13 | 0.49 chao1 | 0.49 | 0.48 mh | 0.48 |
| N50_nw0.2_k3_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.73 jackknife | 0.93 | 0.61 jackknife | 0.91 | 0.72 jackknife | 0.40 | 0.69 jackknife | 0.39 |
| N50_nw0.2_k3_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.77 jackknife | 0.95 | 0.66 jackknife | 0.94 | 0.76 jackknife | 0.35 | 0.73 jackknife | 0.36 |
| N50_nw0.2_k5_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.54 mh | 0.71 | 0.53 mh | 0.57 | 0.74 jackknife | 0.87 | 0.74 jackknife | 0.81 |
| N50_nw0.2_k5_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.53 mh | 0.67 | 0.47 mh | 0.54 | 0.72 jackknife | 0.86 | 0.73 jackknife | 0.83 |
| N50_nw0.2_k5_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.74 jackknife | 0.88 | 0.64 jackknife | 0.82 | 0.48 mh | 0.21 | 0.46 mh | 0.18 |
| N50_nw0.2_k5_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.79 jackknife | 0.90 | 0.70 jackknife | 0.84 | 0.48 mh | 0.17 | 0.47 mh | 0.16 |
| N50_nw0.5_k2_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.27 mh | 0.00 | 0.24 mh | 0.00 | 0.42 chao1 | 0.22 | 0.38 mh | 0.25 |
| N50_nw0.5_k2_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.24 mh | 0.00 | 0.20 mh | 0.00 | 0.41 chao1 | 0.18 | 0.39 mh | 0.20 |
| N50_nw0.5_k2_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.16 chao1 | 0.12 | 0.14 chao1 | 0.07 | 0.67 jackknife | 0.67 | 0.63 jackknife | 0.65 |
| N50_nw0.5_k2_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.17 chao1 | 0.13 | 0.14 chao1 | 0.08 | 0.69 jackknife | 0.66 | 0.63 jackknife | 0.65 |
| N50_nw0.5_k3_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.31 chao1 | 0.00 | 0.29 mh | 0.00 | 0.49 chao1 | 0.51 | 0.45 chao1 | 0.48 |
| N50_nw0.5_k3_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.32 mh | 0.00 | 0.29 mh | 0.00 | 0.48 chao1 | 0.51 | 0.41 chao1 | 0.52 |
| N50_nw0.5_k3_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.08 mh | 0.12 | 0.07 mh | 0.06 | 0.63 jackknife | 0.39 | 0.61 jackknife | 0.38 |
| N50_nw0.5_k3_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.13 mh | 0.17 | 0.11 mh | 0.09 | 0.64 jackknife | 0.42 | 0.60 jackknife | 0.38 |
| N50_nw0.5_k5_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.22 mh | 0.02 | 0.20 mh | 0.01 | 0.60 jackknife | 0.79 | 0.62 jackknife | 0.77 |
| N50_nw0.5_k5_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.26 mh | 0.02 | 0.24 mh | 0.01 | 0.70 jackknife | 0.79 | 0.67 jackknife | 0.76 |
| N50_nw0.5_k5_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.02 chao1 | 0.02 | 0.02 chao1 | 0.01 | 0.42 mh | 0.23 | 0.40 mh | 0.21 |
| N50_nw0.5_k5_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.02 chao1 | 0.02 | 0.02 chao1 | 0.00 | 0.38 mh | 0.21 | 0.38 mh | 0.20 |
| N200_nw0.0_k2_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.69 mh | 0.05 | 0.67 mh | 0.01 | 0.68 mh | 0.01 | 0.67 mh | 0.01 |
| N200_nw0.0_k2_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.67 mh | 0.04 | 0.65 mh | 0.01 | 0.67 mh | 0.01 | 0.65 mh | 0.01 |
| N200_nw0.0_k2_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.98 jackknife | 0.74 | 0.93 mh | 0.89 | 0.94 mh | 0.90 | 0.93 mh | 0.89 |
| N200_nw0.0_k2_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.97 jackknife | 0.73 | 0.92 mh | 0.90 | 0.91 mh | 0.91 | 0.92 mh | 0.90 |
| N200_nw0.0_k3_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.85 chao1 | 0.72 | 0.84 mh | 0.45 | 0.85 mh | 0.48 | 0.84 mh | 0.45 |
| N200_nw0.0_k3_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.81 chao1 | 0.72 | 0.85 chao1 | 0.46 | 0.84 mh | 0.46 | 0.85 chao1 | 0.46 |
| N200_nw0.0_k3_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.92 chao1 | 0.11 | 0.93 chao1 | 0.24 | 0.94 chao1 | 0.24 | 0.93 chao1 | 0.24 |
| N200_nw0.0_k3_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.94 chao1 | 0.09 | 0.93 chao1 | 0.24 | 0.94 chao1 | 0.24 | 0.93 chao1 | 0.24 |
| N200_nw0.0_k5_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.98 jackknife | 1.00 | 0.94 mh | 1.00 | 0.94 mh | 1.00 | 0.94 mh | 1.00 |
| N200_nw0.0_k5_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.97 jackknife | 1.00 | 0.92 mh | 1.00 | 0.92 mh | 0.99 | 0.92 mh | 1.00 |
| N200_nw0.0_k5_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.85 chao1 | 0.01 | 0.84 mh | 0.02 | 0.85 mh | 0.02 | 0.84 mh | 0.02 |
| N200_nw0.0_k5_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.79 chao1 | 0.00 | 0.82 chao1 | 0.01 | 0.83 mh | 0.01 | 0.82 chao1 | 0.01 |
| N200_nw0.2_k2_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.53 chao1 | 0.00 | 0.50 chao1 | 0.00 | 0.56 mh | 0.01 | 0.57 mh | 0.01 |
| N200_nw0.2_k2_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.57 mh | 0.00 | 0.52 mh | 0.00 | 0.63 mh | 0.03 | 0.62 mh | 0.03 |
| N200_nw0.2_k2_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.58 mh | 1.00 | 0.46 mh | 1.00 | 0.92 mh | 0.88 | 0.90 mh | 0.86 |
| N200_nw0.2_k2_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.57 mh | 1.00 | 0.45 mh | 0.99 | 0.91 mh | 0.89 | 0.90 mh | 0.87 |
| N200_nw0.2_k3_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.71 mh | 0.05 | 0.63 mh | 0.01 | 0.76 chao1 | 0.47 | 0.76 mh | 0.46 |
| N200_nw0.2_k3_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.72 mh | 0.05 | 0.67 mh | 0.01 | 0.81 mh | 0.48 | 0.82 chao1 | 0.47 |
| N200_nw0.2_k3_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.90 jackknife | 1.00 | 0.67 jackknife | 1.00 | 0.93 jackknife | 0.34 | 0.92 jackknife | 0.33 |
| N200_nw0.2_k3_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.93 jackknife | 1.00 | 0.76 jackknife | 1.00 | 0.92 jackknife | 0.26 | 0.91 jackknife | 0.25 |
| N200_nw0.2_k5_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.68 mh | 0.75 | 0.59 mh | 0.50 | 0.87 mh | 0.99 | 0.85 mh | 0.99 |
| N200_nw0.2_k5_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.74 mh | 0.78 | 0.60 mh | 0.55 | 0.89 mh | 0.99 | 0.89 mh | 0.99 |
| N200_nw0.2_k5_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.91 jackknife | 0.99 | 0.80 jackknife | 0.98 | 0.80 mh | 0.04 | 0.79 mh | 0.05 |
| N200_nw0.2_k5_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.97 jackknife | 1.00 | 0.90 jackknife | 1.00 | 0.79 chao1 | 0.01 | 0.80 chao1 | 0.02 |
| N200_nw0.5_k2_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.32 chao1 | 0.00 | 0.30 chao1 | 0.00 | 0.53 chao1 | 0.05 | 0.55 chao1 | 0.06 |
| N200_nw0.5_k2_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.38 chao1 | 0.00 | 0.35 chao1 | 0.00 | 0.51 chao1 | 0.05 | 0.52 chao1 | 0.06 |
| N200_nw0.5_k2_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.06 mh | 0.02 | 0.04 mh | 0.00 | 0.85 jackknife | 0.80 | 0.82 jackknife | 0.79 |
| N200_nw0.5_k2_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.03 mh | 0.01 | 0.02 mh | 0.00 | 0.83 jackknife | 0.84 | 0.80 jackknife | 0.81 |
| N200_nw0.5_k3_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.30 mh | 0.00 | 0.25 mh | 0.00 | 0.67 chao1 | 0.50 | 0.66 chao1 | 0.51 |
| N200_nw0.5_k3_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.28 mh | 0.00 | 0.24 mh | 0.00 | 0.65 chao1 | 0.50 | 0.64 mh | 0.49 |
| N200_nw0.5_k3_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.00 mh | 0.00 | 0.00 mh | 0.00 | 0.86 jackknife | 0.33 | 0.84 jackknife | 0.31 |
| N200_nw0.5_k3_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.01 mh | 0.01 | 0.00 mh | 0.00 | 0.87 jackknife | 0.31 | 0.87 jackknife | 0.30 |
| N200_nw0.5_k5_p0.15_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.12 mh | 0.00 | 0.07 chao1 | 0.00 | 0.82 jackknife | 0.98 | 0.82 jackknife | 0.97 |
| N200_nw0.5_k5_p0.15_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.15 mh | 0.00 | 0.10 mh | 0.00 | 0.83 jackknife | 0.98 | 0.83 jackknife | 0.98 |
| N200_nw0.5_k5_p0.4_s0.5_logit_normal_rho0.0_gW0.9_r1.0_f0.0 | 0.00 mh | 0.00 | 0.00 mh | 0.00 | 0.69 mh | 0.09 | 0.68 mh | 0.10 |
| N200_nw0.5_k5_p0.4_s0.5_two_class_rho0.0_gW0.9_r1.0_f0.0 | 0.00 mh | 0.00 | 0.00 mh | 0.00 | 0.69 chao1 | 0.05 | 0.68 chao1 | 0.06 |

## default grid: small-t correction, rel. bias vs U_w, nw = 0, ρ = 0, gold p = 1

| N | k | het | chao1 | chao1_large_t | mh | mh_lee_chao | jackknife |
|---|---|---|---|---|---|---|---|
| 50 | 2 | low | +0.24 | +1.49 | +0.28 | +4.27 | -0.58 |
| 50 | 2 | high | -0.39 | +0.21 | -0.39 | +1.75 | -0.67 |
| 50 | 2 | extreme | -0.79 | -0.58 | -0.79 | +0.06 | -0.78 |
| 50 | 3 | low | +0.05 | +0.58 | +0.13 | +1.57 | -0.19 |
| 50 | 3 | high | -0.38 | -0.08 | -0.33 | +0.47 | -0.44 |
| 50 | 3 | extreme | -0.74 | -0.61 | -0.73 | -0.46 | -0.71 |
| 50 | 5 | low | +0.04 | +0.30 | +0.08 | +0.75 | +0.52 |
| 50 | 5 | high | -0.38 | -0.22 | -0.36 | -0.04 | -0.16 |
| 50 | 5 | extreme | -0.62 | -0.53 | -0.69 | -0.61 | -0.64 |
| 200 | 2 | low | +0.00 | +1.00 | +0.00 | +3.42 | -0.58 |
| 200 | 2 | high | -0.47 | +0.07 | -0.47 | +1.48 | -0.66 |
| 200 | 2 | extreme | -0.84 | -0.67 | -0.84 | -0.13 | -0.78 |
| 200 | 3 | low | -0.04 | +0.44 | +0.01 | +1.44 | -0.18 |
| 200 | 3 | high | -0.46 | -0.19 | -0.41 | +0.36 | -0.43 |
| 200 | 3 | extreme | -0.78 | -0.67 | -0.76 | -0.50 | -0.71 |
| 200 | 5 | low | -0.05 | +0.18 | -0.02 | +0.68 | +0.54 |
| 200 | 5 | high | -0.43 | -0.29 | -0.38 | -0.06 | -0.16 |
| 200 | 5 | extreme | -0.73 | -0.66 | -0.73 | -0.64 | -0.64 |

## ds4 grid: Lincoln–Petersen and residual (LP unseen − mh) bias by g_Z/g_W and false-non-match

| g_Z/g_W | fnm | LP rel bias vs U (median) | LP coverage U (median) | residual bias vs |Z| (median, nw > 0) |
|---|---|---|---|---|
| 0.5 | 0.0 | -0.169 | 0.55 | -0.030 |
| 0.5 | 0.1 | +0.002 | 0.70 | +0.208 |
| 1.0 | 0.0 | +0.000 | 0.91 | +0.469 |
| 1.0 | 0.1 | +0.170 | 0.80 | +0.751 |
| 1.5 | 0.0 | +0.061 | 0.90 | +0.824 |
| 1.5 | 0.1 | +0.274 | 0.58 | +1.159 |
