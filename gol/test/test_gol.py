"""
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

Or:

Any live cell with two or three live neighbours survives.
Any dead cell with three live neighbours becomes a live cell.
All other live cells die in the next generation. Similarly, all other dead cells stay dead.
"""


from hamcrest import *

from gol.gol import Game, dead_cell, living_cell, round_earth_cell_at, GameMaker


class TestLivingCellSurvival:
    _cell = living_cell()

    def test_it_dies_on_one_living_neighbour(self):
        (self._cell.next_generation([living_cell()]).is_alive(), is_(False))

    def test_it_survives_on_two_living_neighbours(self):
        assert_that(
            self._cell.next_generation([living_cell(), living_cell()]).is_alive(),
            is_(True),
        )

    def test_it_dies_on_one_living_and_one_dead_neighbour(self):
        assert_that(
            self._cell.next_generation([living_cell(), dead_cell()]).is_alive(),
            is_(False),
        )

    def test_it_survives_on_three_living_neighbours(self):
        assert_that(
            self._cell.next_generation(
                [living_cell(), living_cell(), living_cell()]
            ).is_alive(),
            is_(True),
        )

    def test_it_dies_on_four_living_neighbours(self):
        assert_that(
            self._cell.next_generation(
                [living_cell(), living_cell(), living_cell(), living_cell()]
            ).is_alive(),
            is_(False),
        )


class TestDeadCellResurrection:
    _cell = dead_cell()

    def test_it_remains_dead_with_two_living_neighbours(self):
        assert_that(
            self._cell.next_generation([living_cell(), living_cell()]).is_alive(),
            is_(False),
        )

    def test_it_resurrects_with_three_living_neighbours(self):
        assert_that(
            self._cell.next_generation(
                [living_cell(), living_cell(), living_cell()]
            ).is_alive(),
            is_(True),
        )

    def test_it_remains_dead_on_one_dead_on_two_living_neighbours(self):
        assert_that(
            dead_cell()
            .next_generation([dead_cell(), living_cell(), living_cell()])
            .is_alive(),
            is_(False),
        )


class TestNeighboursInGame:
    def test_it_has_eight_neighbours_for_non_edge_cells(self):
        game = Game([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert_that(game.neighbours_for(1, 1), is_(equal_to([1, 2, 3, 4, 6, 7, 8, 9])))

    def test_it_has_five_neighbours_for_left_edge_cells(self):
        game = Game([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert_that(game.neighbours_for(1, 0), is_(equal_to([1, 2, 5, 7, 8])))

    def test_it_has_five_neighbours_for_right_edge_cells(self):
        game = Game([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert_that(game.neighbours_for(1, 2), is_(equal_to([2, 3, 5, 8, 9])))

    def test_it_has_five_neighbours_for_top_edge_cells(self):
        game = Game([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert_that(game.neighbours_for(0, 1), is_(equal_to([1, 3, 4, 5, 6])))

    def test_it_has_five_neighbours_for_bottom_edge_cells(self):
        game = Game([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert_that(game.neighbours_for(2, 1), is_(equal_to([4, 5, 6, 7, 9])))

class TestNextGenerationInFlatEarth:
    def test_it_creates_a_new_game_with_a_next_generation_for_all_fields_in_a_row(self):
        game = Game([[living_cell(), living_cell(), living_cell()]])
        game = game.next_generation()
        assert_that(game.cell_at(0, 0), is_(equal_to(dead_cell())))
        assert_that(game.cell_at(0, 1), is_(equal_to(living_cell())))
        assert_that(game.cell_at(0, 2), is_(equal_to(dead_cell())))

class TestNeighboursInRoundEarth:
    _game = game = Game([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ], cell_at_fn=round_earth_cell_at)
    
    def test_it_has_eight_neighbours_for_non_edge_cells(self):
        assert_that(self._game.neighbours_for(1, 1), is_(equal_to([1, 2, 3, 4, 6, 7, 8, 9])))

    def test_it_has_eight_neighbours_for_left_edge_cells(self):
        assert_that(self._game.neighbours_for(1, 0), is_(equal_to([3, 1, 2, 6, 5, 9, 7, 8])))

    def test_it_has_eight_neighbours_for_right_edge_cells(self):
        assert_that(self._game.neighbours_for(1, 2), is_(equal_to([2, 3, 1, 5, 4, 8, 9, 7])))

    def test_it_has_eight_neighbours_for_top_edge_cells(self):
        assert_that(self._game.neighbours_for(0, 1), is_(equal_to([7, 8, 9, 1, 3, 4, 5, 6])))

    def test_it_has_eight_neighbours_for_bottom_edge_cells(self):
        assert_that(self._game.neighbours_for(2, 1), is_(equal_to([4, 5, 6, 7, 9, 1, 2, 3])))

# class TestNextGenerationInRoundEarth:
    # def test_it_creates_a_new_game_with_a_next_generation_for_all_fields_in_a_row(self):
    #     game = Game([[living_cell(), living_cell(), living_cell()]], cell_at_fn=round_earth_cell_at)
    #     game = game.next_generation()
    #     assert_that(game.cell_at(0, 0), is_(equal_to(dead_cell())))
    #     assert_that(game.cell_at(0, 1), is_(equal_to(living_cell())))
    #     assert_that(game.cell_at(0, 2), is_(equal_to(dead_cell())))

class TestGameMaker:

    def test_blinker(self):
        maker = GameMaker()

        game = maker.make_game(3, 3, [(0,1), (1,1), (2,1)])
        expected = Game(
            [
            [dead_cell(), living_cell(), dead_cell()],
            [dead_cell(), living_cell(), dead_cell()],
            [dead_cell(), living_cell(), dead_cell()]
            ])

        assert_that(game, is_(equal_to(expected)))
    
    def test_create_horizontal_blinker(self):
        maker = GameMaker()

        game = maker.make_game(3, 3, [(1, 0), (1, 1), (1, 2)])
        expected = Game(
            [
            [dead_cell(),   dead_cell(),   dead_cell()],
            [living_cell(), living_cell(), living_cell()],
            [dead_cell(),   dead_cell(),   dead_cell()]
            ])

        assert_that(game, is_(equal_to(expected)))