# ===============================
# 1. Load libraries
# ===============================
library(readr)
library(dplyr)

# ===============================
# 2. Define path
# ===============================
train_path <- "C:/projetR/House Pricing R/data/Raw/train.csv"
test_path  <- "C:/projetR/House Pricing R/data/Raw/test.csv"

# ===============================
# 3. Import data
# ===============================
train <- read_csv(train_path)
test  <- read_csv(test_path)

# ===============================
# 4. First check
# ===============================
print(dim(train))   # rows, columns
print(dim(test))

head(train)

# ===============================
# Understanding of dataset
# ===============================

#structure of dataset
str(train)

summary(train)

# Count missing values per column
missing_values <- colSums(is.na(train))

# Show only columns with missing values
missing_values[missing_values > 0]

# Distribution of SalePrice
summary(train$SalePrice)
hist(train$SalePrice, col="blue", main="Distribution of SalePrice")
