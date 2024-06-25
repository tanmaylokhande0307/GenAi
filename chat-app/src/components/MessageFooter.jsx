import { Box } from "@mui/material";
import { displayTime } from "../shared/utils";

export const MessageFooter = () => {
  return (
    <Box
      sx={{
        display: "inline",
        marginLeft: "auto",
        marginBottom: "5px",
        transform: "translate(8px, 10px)",
      }}
    >
      <p
        style={{
          display: "flex",
          alignItems: "center",
          gap: "0.5px",
          fontSize: "14px",
          fontWeight: 400,
          lineHeight: 1.43,
          marginTop: "5px",
          marginBottom: "5px",
        }}
      >
        {displayTime()}
      </p>
    </Box>
  );
};
