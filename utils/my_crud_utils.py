import mptt

def category_belonging_dict(belongingObject, ManyRelatedManagerName):
    """Create a dictionary of MPTT category belonging
    Given the name of an MPTTModel that defines hierarchical categories
    and an object that has belonging of one or more of those categories,
    return a dictionary of categories the object belongs to
    If the MPTT model is say 'Skill', then the ManyRelatedManagerName
    will by default be 'skills', i.e. it is the name used in defining the
    relationship between the model of the category-belonging object and the
    category model with for eg:
    skills = models.ManyToManyField(Skill)
    In django terminology, skills is of type ManyRelatedManager
    """
    catDict = {}
    cats = getattr(belongingObject,ManyRelatedManagerName)
    if cats.all().count != 0:
        mpttCats = mptt.utils.tree_item_iterator(cats.all(), ancestors=False)
        for cat in mpttCats:
             catDict[cat[0].name] = cat[0].name
    return catDict
