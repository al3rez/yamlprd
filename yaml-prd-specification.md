# YAML PRD Specification

## Why YAML PRDs

YAML PRDs reduce token consumption by 40-60% and eliminate hallucination risks through structured, machine-readable specifications.

### Key Benefits
1. **Token Efficiency**: Hierarchical key-value structure without filler words
2. **Zero Ambiguity**: Explicit values prevent misinterpretation
3. **Machine-Readable**: Native parsing, consistent structure, type safety
4. **Version Control**: Line-by-line diffs, easy merges, inline comments

## Core Structure

```yaml
prd:
  title: string
  purpose: string
  features:
    - id: string
      user_story: string
  metrics:
    - metric: string
      target: string
  constraints:
    - string
```

## Example: Virtual Try-On Marketplace

```yaml
prd:
  title: Virtual Try-On Clothing Marketplace
  purpose: Allow users to sell clothes and try on outfits virtually using AI
  
  features:
    - id: F1
      user_story: "As a user, I can list clothes for sale with images and details"
    - id: F2  
      user_story: "As a user, I can try on clothes virtually using my photo"
    - id: F3
      user_story: "As a user, I can purchase clothes from other users"
  
  metrics:
    - metric: TryOn_Engagement_Rate
      target: "60% of users complete first try-on"
    - metric: Listing_Conversion
      target: "40% of items sold within 30 days"
  
  constraints:
    - "5 free try-ons per user"
    - "One full-body photo per account"
    - "10MB max image size"
```

## Best Practices

### Keep It DRY
```yaml
# Use references for repeated structures
definitions:
  &user_fields
    id: uuid
    email: string

schemas:
  user: *user_fields
  seller: 
    <<: *user_fields
    listings: array
```

### Be Explicit
```yaml
timeout_seconds: 30  # Not just "timeout: 30"
max_file_size_mb: 10  # Not just "size: 10"
```

## Converting PDFs to YAML PRDs

### Tools
- **Web**: https://pdf2md.morethan.io/ - Convert PDF to Markdown online
- **CLI**: `pip install pdf2markdown4llm` - Convert PDF to LLM-friendly Markdown

### Workflow
1. Convert PDF PRD to Markdown using above tools
2. Extract key information into YAML structure
3. Validate with AI assistant for completeness

## Results

| Metric | YAML PRD | Traditional PRD |
|--------|----------|-----------------|
| Tokens | 500-1000 | 2000-5000 |
| AI Accuracy | 100% | 70-85% |
| Update Time | Seconds | Hours |

## Extended Structure (When Needed)

```yaml
prd:
  # Core fields as above
  
  technical_specs:  # Optional
    api:
      - endpoint: /api/v1/resource
        method: POST
    database:
      table_name:
        column: type
  
  dependencies:  # Optional
    - name: service_name
      version: ">=1.0"
  
  testing:  # Optional
    coverage: 80
    scenarios:
      - name: string
```