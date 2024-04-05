
# Software Engineer (ML & LLMs) Challenge Report

## 1. Model Selection

### Objective
The aim of this report is to summarize the process of selecting the most appropriate model for the given task based on experimental results and evaluation metrics.

### Dataset Description
The dataset consists of 45,698 instances with 37 features, divided into a training set with 45,698 instances and a test set with 22,508 instances. The target variable is binary, representing whether an event occurred or not.

### Model Evaluation
Several versions of XGBoost and Logistic Regression classifiers were trained and evaluated on the test set.

### Findings
1. **Performance Comparison:**
   - XGBoost and Logistic Regression models exhibited similar performance across various metrics.
   - `xgb_model_2` showed significantly improved recall for the minority class.

2. **Feature Reduction:**
   - Reducing features to the top 10 most important did not negatively impact model performance.

3. **Class Imbalance Handling:**
   - Balancing classes, particularly in `xgb_model_2`, led to notable improvement in minority class recall.

### Selected Model
Based on evaluation metrics and experimental findings, `xgb_model_2` was chosen as the most suitable model.

### Conclusion
`xgb_model_2` provides a balanced performance and effective class imbalance handling.

### Recommendations
- Consider hyperparameter fine-tuning for potential improvements.
- Monitor model performance on unseen data for iteration.

### Model Selection Summary

After thorough experimentation, `xgb_model_2` emerged as the most suitable model, striking a balance between performance and effective class imbalance handling. Feature reduction experiments affirmed the informativeness of selected features. `xgb_model_2` lays the foundation for further optimization and refinement.

## 2. Testing Adjustments

### Issue
Problems were encountered while reading the `data.csv` file in the `test_model.py` test script.

### Resolution
Adjusted file path to resolve file reading issue.

```python
# def setUp(self) -> None:
#     super().setUp()
#     self.model = DelayModel()
#     self.data = pd.read_csv(filepath_or_buffer="../data/data.csv")

def setUp(self) -> None:
    super().setUp()
    self.model = DelayModel()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "../../data/data.csv")
    self.data = pd.read_csv(filepath_or_buffer=data_path)
```

## 3. GitHub Actions Workflow

### Issue
Sequential execution of workflows (`ci.yml` followed by `cd.yml`) failed due to malfunctioning commands.

### Resolution
Both workflows (`ci.yml` and `cd.yml`) are executed in parallel upon completion of Continuous Integration workflow.

```yaml
on:
  workflow_run:
    workflows: [Continuous Integration]
    types:
      - completed
```
