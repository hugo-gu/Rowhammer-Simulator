`timescale 1ns/1ps
module attacker #(
    parameter [7:0] AGG0 = 8'd127,
    parameter [7:0] AGG1 = 8'd129
)(
    input  wire       clk,
    input  wire       rst,
    output reg        activate,
    output reg  [7:0] row
);
    always @(posedge clk) begin
        if (rst) begin
            activate <= 1'b0;
            row <= AGG0;
        end else begin

            activate <= 1'b1;
            if (row == AGG0)
                row <= AGG1;
            else
                row <= AGG0;
        end
    end
endmodule