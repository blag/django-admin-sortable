from .models import SortableMixin, SortableForeignKey


def check_inheritance(cls):
    return issubclass(type(cls), SortableMixin)


def get_is_sortable(objects):
    if objects.count() < 2:
        return False

    if not check_inheritance(objects[:1][0]):
        return False

    return True


def is_self_referential(cls):
    cls_type = type(cls)
    sortable_subclass = check_inheritance(cls_type)
    sortable_foreign_key_subclass = issubclass(cls_type, SortableForeignKey)
    if sortable_foreign_key_subclass and not sortable_subclass:
        return True
    return False


def check_model_is_sortable(cls):
    if cls:
        if check_inheritance(cls):
            if is_self_referential(cls):
                objects = cls.model.objects
            else:
                objects = cls.objects
            return get_is_sortable(objects.all())
    return False


# def diff(old_list: Iterable, new_list: Iterable) -> Union[None, Tuple[int, int]]:
def diff(old_list, new_list):
    """
    Returns: None if the element didn't move, or a tuple of (old position, new position) if it has
    ASSUMPTIONS:
      1. All elements exist in both lists
      2. Only one element has moved
    """
    # state values:
    #  0 = comparing lists, starting from the front
    #  1 = detected element moved backwards (eg: higher index), scanning new_list for old element
    # -1 = detected element moved forwards (eg: lower index), scanning old_list for old element
    state = 0  # comparing lists
    for i in range(len(old_list)):
        # Compare lists, starting at the front
        if state == 0:  # comparing lists
            # If the elements are different, we've either found where the
            # moved element was removed from the old list or where the moved
            # element was inserted into the new list
            if old_list[i] != new_list[i]:
                if i < (len(old_list) - 1) and old_list[i + 1] == new_list[i]:
                    old_element_position = i
                    state = 1  # element moved backwards

                elif i < (len(new_list) - 1) and new_list[i + 1] == old_list[i]:
                    new_element_position = i
                    state = -1  # element moved forwards

        elif state == 1:  # element moved backwards
            if old_list[old_element_position] == new_list[i]:
                new_element_position = i
                break

        elif state == -1:  # element moved forwards
            if new_list[new_element_position] == old_list[i]:
                old_element_position = i
                break

    else:
        # If we made it through the entire list then the element wasn't moved
        return None

    return (old_element_position, new_element_position)
