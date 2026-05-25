# ============================================================

# STEP 5 BIS — CLEAN & TRANSFORM TEST DATA (R)

# ============================================================

# Objective:

# - Apply SAME cleaning as train dataset

# - Prepare test data for prediction in Python

# ============================================================

# ===============================

# 1. Check missing values

# ===============================

missing_values_test <- colSums(is.na(test))
missing_values_test[missing_values_test > 0]

# ------------------------------------------------------------

# Identify missing values in test dataset

# ------------------------------------------------------------

# ===============================

# 2. Remove unnecessary column

# ===============================

# Remove Alley (same as train)

test$Alley <- NULL

# ------------------------------------------------------------

# Alley has too many missing values

# ------------------------------------------------------------

# ===============================

# 3. Feature Engineering

# ===============================

# Create Total Surface variable

test$TotalSF <- test$GrLivArea + test$TotalBsmtSF

# ------------------------------------------------------------

# Same feature as train (VERY IMPORTANT)

# ------------------------------------------------------------

# ===============================

# 4. Handle missing values (KNN)

# ===============================

library(VIM)

# Apply KNN imputation

test_knn <- kNN(test, k = 5)

# Remove helper columns created by kNN

test_knn <- test_knn[, !grepl("_imp", names(test_knn))]

# Replace original dataset

test <- test_knn

# ------------------------------------------------------------

# KNN fills missing values using nearest neighbors

# ------------------------------------------------------------

# ===============================

# 5. Convert categorical variables

# ===============================

library(dplyr)

# Convert all character variables to factors

test <- test %>%
  mutate(across(where(is.character), as.factor))

# ------------------------------------------------------------

# Ensure same structure as train

# ------------------------------------------------------------

# ===============================

# 6. Final check

# ===============================

# Check missing values

colSums(is.na(test))

# Check structure

str(test)

# Preview dataset

head(test)

# ------------------------------------------------------------

# Ensure data is clean and consistent

# ------------------------------------------------------------

# ===============================

# 7. Export cleaned test dataset

# ===============================

write.csv(test, "C:/projetR/House Pricing R/data/Cleaned/test_clean.csv", row.names = FALSE)

# ------------------------------------------------------------

# Save dataset for Python modeling

# ------------------------------------------------------------
