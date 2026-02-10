#include "./include/parse_boards.h"

float create_board(const uint64_t bbs[2][6])
{
    float board_tensor[12][8][8] = {0.0f};
    for (int piece = 0; piece < 12; piece++)
    {
        uint64_t bb = bbs[piece / 6][piece % 6];
        for (int square = 0; square < 64; square++)
        {
            if (bb & (1ULL << square))
            {
                int row = square / 8;
                int col = square % 8;
                board_tensor[piece][row][col] = 1.0f;
            }
        }
    }
    return board_tensor;
}