from auth.permissions import Permission, PermissionSet, check_permission


def test_add_and_has():
    ps = PermissionSet()
    ps.add(Permission.READ)
    assert ps.has(Permission.READ) is True
    assert ps.has(Permission.WRITE) is False


def test_remove():
    ps = PermissionSet({Permission.READ, Permission.WRITE})
    ps.remove(Permission.READ)
    assert ps.has(Permission.READ) is False
    assert ps.has(Permission.WRITE) is True


def test_remove_nonexistent():
    ps = PermissionSet()
    ps.remove(Permission.ADMIN)
    assert len(ps) == 0


def test_intersection():
    a = PermissionSet({Permission.READ, Permission.WRITE, Permission.DELETE})
    b = PermissionSet({Permission.READ, Permission.ADMIN})
    result = a.intersection(b)
    assert result.has(Permission.READ) is True
    assert result.has(Permission.WRITE) is False
    assert len(result) == 1


def test_intersection_with_empty():
    a = PermissionSet({Permission.READ, Permission.WRITE})
    b = PermissionSet()
    result = a.intersection(b)
    assert len(result) == 0


def test_union():
    a = PermissionSet({Permission.READ})
    b = PermissionSet({Permission.WRITE})
    result = a.union(b)
    assert result.has(Permission.READ) is True
    assert result.has(Permission.WRITE) is True


def test_check_permission_admin_bypass():
    perms = PermissionSet({Permission.ADMIN})
    assert check_permission(perms, Permission.DELETE) is True
    assert check_permission(perms, Permission.WRITE) is True


def test_check_permission_specific():
    perms = PermissionSet({Permission.READ})
    assert check_permission(perms, Permission.READ) is True
    assert check_permission(perms, Permission.WRITE) is False


def test_len():
    ps = PermissionSet({Permission.READ, Permission.WRITE})
    assert len(ps) == 2


def test_iter():
    perms = {Permission.READ, Permission.EXECUTE}
    ps = PermissionSet(perms)
    assert set(ps) == perms
