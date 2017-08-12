RANGE_CHOICES = (
    (1,'Within 1 mile'),
    (2,'Within 2 miles'),
    (5,'Within 5 miles')
)


MR = 'MR'
MRS = 'MRS'
MS = 'MS'
SIR = 'SIR'
TITLE_CHOICES = (
    (MR, 'Mr'),
    (MRS, 'Mrs'),
    (MS, 'Ms'),
    (SIR, 'Sir'),
)

MALE = 'MALE'
FEMALE = 'FEMALE'
SEX_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)

#choices for stages of a project
PROPOSED = 'PROP'
CURRENT = 'CURR'
COMPLETED = 'COMP'
STAGE_CHOICES = (
    (PROPOSED, 'Proposed'),
    (CURRENT, 'Current'),
    (COMPLETED, 'Completed'),
)
