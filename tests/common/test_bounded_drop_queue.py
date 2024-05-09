from retrochatbot.framework.common.bounded_drop_queue import BoundedDropQueue


def test_old_items_dropped():
    queue: BoundedDropQueue[str] = BoundedDropQueue(max_size=3)
    queue.append("a")
    assert queue.data == ["a"]
    queue.append("b")
    assert queue.data == ["a", "b"]
    queue.append("c")
    assert queue.data == ["a", "b", "c"]
    queue.append("d")
    assert queue.data == ["b", "c", "d"]
    queue.append("e")
    assert queue.data == ["c", "d", "e"]


def test_data_is_immutable():
    queue: BoundedDropQueue[str] = BoundedDropQueue(max_size=3)
    queue.append("a")
    data_copy: list[str] = queue.data
    data_copy.append("b")
    assert queue.data == ["a"]


def test_size_up():
    queue: BoundedDropQueue[str] = BoundedDropQueue(max_size=3)
    queue.append("a")
    queue.append("b")
    queue.append("c")
    assert queue.data == ["a", "b", "c"]
    queue.resize(max_size=5)
    assert queue.data == ["a", "b", "c"]


def test_size_down():
    queue: BoundedDropQueue[str] = BoundedDropQueue(max_size=3)
    queue.append("a")
    queue.append("b")
    queue.append("c")
    assert queue.data == ["a", "b", "c"]
    queue.resize(max_size=2)
    assert queue.data == ["b", "c"]
