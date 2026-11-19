`timescale 1ns/1ps
module attacker #(
    parameter [7:0] AGG0 = 8'd127,   // one aggressor row (victim - 1)
    parameter [7:0] AGG1 = 8'd129    // the other aggressor (victim + 1)
)(
    input  wire       clk,
    input  wire       rst,
    output reg        activate,      // 1 = "activate a row this cycle"
    output reg  [7:0] row            // which row to activate
);
    always @(posedge clk) begin
        if (rst) begin
            // TODO: starting state — not activating yet; row = AGG0
            activate <= 1'b0;
            row <= AGG0;
        end else begin
            // TODO: every cycle, assert activate=1 and flip row
            //       between AGG0 and AGG1
            activate <= 1'b1;
            if (row == AGG0)
                row <= AGG1;
            else
                row <= AGG0;
        end
    end
endmodule