def get_pokenature_by_id(nature_id: int, stat_num: int): 
    """
    This function gets a nature id, and returns either 100, 90, or 110 for immediate use in stat calculations.
    The "order" of natures was explicitly done so that this modulo magic can happen. 
    Note that if the stat_num equals increase and decrease, this is a "neutral" nature.
    """ 
    increase = (nature_id - 1) // 5
    decrease = (nature_id - 1) % 5

    return 100 + 10 * (stat_num == increase) - 10 * (stat_num == decrease) 