## Description
This merge request improves the FAQ retrieval accuracy by refining the embedding normalization process and optimizing FAISS index creation.

## Related Issue
Closes #12 (Inaccurate FAQ retrieval for large datasets)

## Changes Made
- Optimized sentence embedding generation
- Improved cosine similarity normalization
- Added validation for empty or malformed FAQ entries
- Updated documentation for supported file formats

## Testing Performed
- Tested with CSV files containing 50, 500, and 1500 FAQs
- Verified semantic similarity search accuracy
- Manually validated answers for HR and Banking datasets

## Checklist
- [x] Code follows project standards
- [x] Documentation updated
- [x] Tested locally
- [ ] Requires additional performance benchmarking
