
# Load libraries
library(tidyr)
library(dplyr)
library(ggplot2)
library(stringr)
library(scales)

# Import project data
project_data <- read.csv("DSE5002/R Project/r_project_data.csv")


updated_data <- project_data
# Changing all foreign employee residence to "Offshore"
updated_data$employee_residence[updated_data$employee_residence!="US"] <- "Offshore"
# Changing all foreign company location to "Offshore"
updated_data$company_location[updated_data$company_location!="US"] <- "Offshore"
# Remove all observations that are part-time
updated_data <- updated_data[updated_data$employment_type == "FT", ]

# Median salary by company location for senior level data scientists at small and medium sized companies
senior_level <- 
  updated_data %>%
  filter(experience_level == "SE" & company_size != "L") %>%
  group_by(company_location) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# Median salary by company location for executive level data scientists at small and medium size companies
executive_level <- 
  updated_data %>%
  filter(experience_level == "EX" & company_size != "L") %>%
  group_by(company_location) %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# Find median salary by company size and experience for senior and executive level scientists
experience_data <- 
  updated_data %>%
  filter(experience_level %in% c("SE", "EX") & company_size != "L")  %>%
  group_by(company_size, experience_level)  %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# Create bar plot to compare different exp levels at different sized companies
experience_data %>%
  ggplot(
    mapping = aes(x=experience_level,y=median_salary_usd)
  ) + 
  geom_col(aes(fill = company_size), width = 0.5, position = "dodge") +
  coord_cartesian(ylim = c(75000,200000)) +
  scale_y_continuous(labels = scales::dollar_format()) +
  labs(x='Experience Level',
       y='Median Salary (USD)',
       title='Global Salaries for Senior to Executive-Level Data Scientists 2020-2022')
# group senior level scientists with leadership experience by company size
managers <- 
  updated_data %>%
  filter(grepl("manager|lead", job_title, ignore.case = T) & experience_level == "SE" & company_size != "L") %>%
  group_by(company_size)

# Find median salaries for managers
managers_global <- 
  managers %>%
  summarise(median_salary_usd = median(salary_in_usd), n = n())

# Create a box plot comparing ranges of manager salaries at medium and small sized companies
managers %>%
  ggplot(mapping = aes(x=company_size, y=salary_in_usd, fill = company_size)) +
  stat_boxplot(width = 0.15) +
  geom_boxplot() +
  labs(x='Company Size',
       y='Median Salary (USD)',
       title='Global Salary Ranges for Senior-Level Managers or Leaders 2020-2022') +
  scale_y_continuous(labels = scales::dollar_format()) +
  geom_text(data = managers_global, 
            aes(x=company_size, y = median_salary_usd, label = dollar(median_salary_usd)), 
            position = position_dodge(width = 0.8), 
            size = 3, 
            vjust = -0.5)

# Find manager salaries by region of residence
managers_region_year <- 
  managers %>%
  group_by(work_year, employee_residence) %>%
  summarise(median_salary_usd = median(salary_in_usd), n =n())

# Create bar plot to show difference in median salary by employee residence and year
managers_region_year %>%
  ggplot(mapping = aes(x=work_year,y=median_salary_usd)) + 
  geom_col(aes(fill = employee_residence), width = 0.5, position = "dodge") +
  coord_cartesian(ylim = c(100000,200000)) +
  scale_y_continuous(labels = scales::dollar_format()) +
  scale_fill_manual(values=c("orange2", "violet")) +
  scale_x_continuous(breaks = seq(min(managers_region_year$work_year), max(managers_region_year$work_year), by=1)) +
  labs(x='Year',
       y='Median Salary (USD)',
       title='Salaries of Senior Level Manager and Lead Data Scientists 2020-2022')

managers_region <- 
  managers %>%
  group_by(employee_residence) %>%
  summarise(median_salary_usd = median(salary_in_usd), n =  n())

# Create boxplot showing ranges of manager salaries by residence
managers %>%
  group_by(employee_residence) %>%
  ggplot(mapping = aes(x=employee_residence, y=salary_in_usd, fill=employee_residence)) +
  stat_boxplot(width = 0.15) +
  geom_boxplot() +
  scale_y_continuous(labels = scales::dollar_format()) +
  scale_fill_manual(values=c("orange2", "violet")) +
  labs(x='Employee Residence',
       y='Median Salary (USD)',
       title='Salary Range for Senior Level Managers and Lead Scientists 2020-2022') +
  geom_text(data = managers_region, 
            aes(x=employee_residence, y = median_salary_usd, label = dollar(median_salary_usd)), 
            position = position_dodge(width = 0.8), 
            size = 3, 
            vjust = -0.5)
  
