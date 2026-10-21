Technical fixes are complete and validated; the planned eight-pair estimate remains blocked by unit D’s missing treatment value.

The script now handles `NA` explicitly. Synthetic calculation checks passed, and supplied data and methods remain unchanged. Run details are saved in [analysis_status.json](outputs/analysis_status.json); no numerical estimate was produced.

Decision needed: keep the analysis pending or authorize a missing-data method. Excluding D would change the analysis population to seven complete pairs.