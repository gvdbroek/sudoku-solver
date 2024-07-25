const std = @import("std");

const Invalid = error{Empty};

pub fn get_row(board: []Invalid!u8, idx: usize) []Invalid!u8 {
    const row: []Invalid!u8 = board[(9 * idx)..((idx + 1) * 9)];
    return row;
}

pub fn load_board(filename: []const u8) ![81]Invalid!u8 {
    // const realPath: []u8 = std.fs.cwd().realpath(filename);
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    var f = try std.fs.cwd().openFile(filename, .{});
    defer f.close();

    const buffer: []u8 = try f.readToEndAlloc(allocator, std.math.maxInt(usize));
    defer allocator.free(buffer);
    std.debug.print("Loaded data into memory:\n", .{});

    var board: [9 * 9]Invalid!u8 = undefined;
    for (0..(9 * 9), 0..) |_, i| {
        const ch: u8 = buffer[i];
        const newline: u8 = '\n';
        if (ch == newline) {
            continue;
        }
        board[i] = std.fmt.parseInt(u8, buffer[i .. i + 1], 10) catch Invalid.Empty;
    }

    // std.debug.print("\n", .{});
    return board;

    // std.debug.print("Checking for file @ {}", .{realPath});

    // std.fs.openFileAbsolute(absolute_path: []const u8, flags: File.OpenFlags)
}

pub fn print_value(value: Invalid!u8) void {
    // var c: u8 = 0;
    if (value) |v| {
        // c = std.fmt.digitToChar(v, 10);
        std.debug.print("{d}", .{v});
    } else |_| {
        // c = '-';
        std.debug.print("-", .{});
    }
}
pub fn print_series(series: []Invalid!u8) void {
    for (series) |value| {
        print_value(value);
    }
    std.debug.print("\n", .{});
}

pub fn main() !void {
    // var board: [9][9]u8 = [9][9]u8();
    //
    const sudoku_file = "../boards/test_grid_1.txt";

    var board = try load_board(sudoku_file);
    var row = get_row(&board, 0);
    print_series(row);
    // std.debug.print("{!s}", .{row});
    board[0] = 1;
    row[0] = 1;
}
