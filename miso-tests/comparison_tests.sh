#!/bin/bash
#compare_miso --compare-samples ./miso_output/KH2_NoDox ./miso_output/KH2_DOX ./comparisons

filter_events --filter comparisons/KH2_NoDox_vs_KH2_DOX/bayes-factors/KH2_NoDox_vs_KH2_DOX.miso_bf --bayes-factor 10 --output-dir ./filtered_comparisons/