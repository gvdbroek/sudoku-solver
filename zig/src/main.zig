const std = @import("std");

pub fn load_board(filename: []const u8) !void {
    // const realPath: []u8 = std.fs.cwd().realpath(filename);
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    var f = try std.fs.cwd().openFile(filename, .{});
    defer f.close();

    const buffer: []u8 = try f.readToEndAlloc(allocator, std.math.maxInt(usize));
    defer allocator.free(buffer);
    std.debug.print("Loaded data into memory:\n", .{});

    for (buffer) |char| {
        if (char == '\n') {
            continue;
        }
        std.debug.print("{c}", .{char});
    }
    std.debug.print("\n", .{});
    // std.debug.print("Checking for file @ {}", .{realPath});

    // std.fs.openFileAbsolute(absolute_path: []const u8, flags: File.OpenFlags)
}

pub fn main() !void {
    // var board: [9][9]u8 = [9][9]u8();
    //
    const sudoku_file = "../boards/test_grid_1.txt";

    try load_board(sudoku_file);
}
