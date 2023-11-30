from warship import Block, Warship


def test_create_block_standard():
    block = Block("A", 8)
    assert block.x == "A"
    assert block.y == 8


def test_create_warship_standard():
    blocks = [
        Block("A", 1), Block("A", 2), Block("A", 3)
    ]
    warship = Warship(blocks)
    assert warship.size == 3
    assert warship.blocks == blocks
