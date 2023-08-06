
# Load libraries
library(tidyr)
library(dplyr)
library(ggplot2)
library(stringr)
library(scales)

# Import project data
project_data <- read.csv("R Project/r_project_data.csv")


updated_data <- project_data
# Changing all foreign employee residence to "Offshore"
updated_data$company_location[updated_data$employee_residence!="US"] <- "Offshore"
# Changing all foreign company location to "Offshore"
updated_data$company_location[updated_data$company_location!="US"] <- "Offshore"
# Remove all observations that are part-time
updated_data <- updated_data[updated_data$employment_type == "FT", ]

# Median salary by company location for senior level data scientists at small and medium sized companies
senior_level <- 
  updated_data %>%
  filter(experience_level == "SE", company_size != "L") %>%
  group_by(company_location) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

executive_level <- 
  updated_data %>%
  filter(experience_level == "EX", company_size != "L") %>%
  group_by(company_location) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

experience_data <- 
  updated_data %>%
  filter(experience_level == c("SE", "EX"), company_size != "L") %>%
  group_by(company_location) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# median salary by company size for offshore data scientists
salary_size_offshore <- 
  updated_data %>%
  filter(experience_level == "SE", company_size != "L", employee_residence == "Offshore") %>%
  group_by(company_size) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# Median salary by company size for all US data scientists
salary_size_us <- 
  updated_data %>%
  filter(experience_level == "SE", company_size != "L", employee_residence == "US") %>%
  group_by(company_size) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# Median salary by remote ratio for US data scientists
salary_remote <- 
  updated_data %>%
  filter(experience_level == "SE", company_size != "L", employee_residence == "US") %>%
  group_by(remote_ratio) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# Median salary by year
salary_year <- 
  updated_data %>%
  select(!c("employment_type", "job_title", "salary", "salary_currency")) %>%
  filter(experience_level == "SE", company_size != "L") %>%
  group_by(work_year, company_location) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

managers <- 
  updated_data %>%
  filter(grepl("manager|lead", job_title, ignore.case = T), experience_level == "SE", company_size != "L") %>%
  group_by(company_size) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())