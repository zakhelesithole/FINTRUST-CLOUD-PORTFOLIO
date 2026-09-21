
# Week 8 Day 4 - AI Pipelines with Rekognition and Comprehend

## Synchronous vs Async Services

| Characteristic | Rekognition / Comprehend | Athena / EMR |
|----------------|--------------------------|--------------|
| Response model | Synchronous | Asynchronous |
| Typical latency | 100ms - 2s | Seconds to minutes |
| Input size limit | Rekognition: 5MB inline / S3. Comprehend: 100KB | Query can span terabytes |
| Pricing model | Per API call | Per TB scanned |

## Rekognition KYC Face Comparison

### Input Options

| Option | Format | Max Size |
|--------|--------|----------|
| Inline bytes | `{'Bytes': b'...'}` | 5 MB |
| S3 reference | `{'S3Object': {'Bucket': '...', 'Name': '...'}}` | No limit |

**Production recommendation:** Use S3 references, not inline bytes. The image is already in S3, so the reference avoids downloading and re-uploading.

### CompareFaces Function

```python
response = rek.compare_faces(
    SourceImage={'S3Object': {'Bucket': selfie_bucket, 'Name': selfie_key}},
    TargetImage={'S3Object': {'Bucket': id_bucket, 'Name': id_key}},
    SimilarityThreshold=95.0
)
