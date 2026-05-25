# ============================================================
# STEP 4 — DATA CLEANING & TRANSFORMATION (FINAL VERSION)
# ============================================================
# Objective:
# - Handle missing values (KNN)
# - Remove irrelevant variables
# - Treat outliers
# - Transform target variable
# - Create new variables
# ============================================================


# ===============================
# 1. Check missing values
# ===============================
missing_values <- colSums(is.na(train))
missing_values[missing_values > 0]

# ------------------------------------------------------------
# Identify which columns contain missing data
# ------------------------------------------------------------



# ===============================
# 2. Remove highly missing column
# ===============================

# Remove Alley (too many missing values)
train$Alley <- NULL

# ------------------------------------------------------------
# Alley has too many missing values, so it is removed
# ------------------------------------------------------------



# ===============================
# 3. Feature Engineering
# ===============================

# Create Total Surface variable
train$TotalSF <- train$GrLivArea + train$TotalBsmtSF

# ------------------------------------------------------------
# This variable combines two important features into one
# ------------------------------------------------------------



# ===============================
# 4. Handle Outliers
# ===============================

# Visualize outliers
plot(train$GrLivArea, train$SalePrice,
     main = "GrLivArea vs SalePrice",
     xlab = "GrLivArea",
     ylab = "SalePrice")

# Remove extreme values
train <- train[train$GrLivArea < 4000, ]

# ------------------------------------------------------------
# Remove unrealistic houses with very large surface
# ------------------------------------------------------------



# ===============================
# 5. KNN Imputation (Advanced but acceptable)
# ===============================

library(VIM)

# Apply KNN imputation
train_knn <- kNN(train, k = 5)

# Remove additional columns created by kNN (_imp)
train_knn <- train_knn[, !grepl("_imp", names(train_knn))]

# Replace original dataset
train <- train_knn

# ------------------------------------------------------------
# KNN fills missing values based on similarity between observations
# ------------------------------------------------------------



# ===============================
# 6. Convert categorical variables to factors
# ===============================

# Convert all character variables to factors
train <- train %>%
  mutate(across(where(is.character), as.factor))

# ------------------------------------------------------------
# Factors are the correct format for categorical variables in R
# ------------------------------------------------------------



# ===============================
# 7. Transform target variable
# ===============================

# Apply log transformation to SalePrice
train$SalePrice <- log(train$SalePrice)

# ------------------------------------------------------------
# Makes distribution more normal and improves model performance
# ------------------------------------------------------------



# ===============================
# 8. Final Check
# ===============================

# Check missing values again
colSums(is.na(train))

# Check structure
str(train)

# Preview cleaned data
head(train)

# ------------------------------------------------------------
# Ensure data is clean and ready for export
# ------------------------------------------------------------

# ===============================
# STEP 5 — Export cleaned dataset
# ===============================

write.csv(train, "C:/projetR/House Pricing R/data/Cleaned/train_clean.csv", row.names = FALSE)
