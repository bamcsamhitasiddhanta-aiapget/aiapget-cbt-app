import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { FC, ReactElement, useEffect, useState } from "react";

export type MyComponentStateShape = {
  expired: boolean;
};

export type MyComponentDataShape = {
  end_time: number;
  total_time: number;
};

export type MyComponentProps = Pick<
  FrontendRendererArgs<MyComponentStateShape, MyComponentDataShape>,
  "setStateValue"
> &
  MyComponentDataShape;

const MyComponent: FC<MyComponentProps> = ({
  end_time,
  total_time,
  setStateValue,
}): ReactElement => {
  const getRemaining = () =>
    Math.max(0, Math.floor(end_time - Date.now() / 1000));

  const [remaining, setRemaining] = useState(getRemaining());
  const percent = (remaining / total_time) * 100;

  useEffect(() => {
    const timer = setInterval(() => {
      const secs = getRemaining();

      setRemaining(secs);

      if (secs <= 0) {
        clearInterval(timer);
        setStateValue("expired", true);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [end_time, setStateValue]);

  const minutes = Math.floor(remaining / 60)
    .toString()
    .padStart(2, "0");

  const seconds = (remaining % 60)
    .toString()
    .padStart(2, "0");

  const hours = Math.floor(remaining / 3600)
    .toString()
    .padStart(2, "0");

  const color =
    percent > 25
      ? "#16a34a"
      : percent > 10
        ? "#f59e0b"
        : "#dc2626";

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "500px",
        margin: "10px auto",
        padding: "18px",
        borderRadius: "14px",
        background: "#ffffff",
        boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
        textAlign: "center",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          fontSize: "15px",
          fontWeight: 700,
          color: "#555",
          marginBottom: "10px",
        }}
      >
        ⏳ TIME REMAINING
      </div>

      <div
        style={{
          fontSize: "42px",
          fontWeight: "bold",
          color: color,
          marginBottom: "16px",
        }}
      >
        {hours}:{minutes}:{seconds}
      </div>

      <div
        style={{
          width: "100%",
          height: "14px",
          background: "#e5e7eb",
          borderRadius: "8px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${percent}%`,
            height: "100%",
            background: color,
            transition: "width 1s linear",
          }}
        />
      </div>

      <div
        style={{
          marginTop: "8px",
          fontSize: "13px",
          color: "#666",
        }}
      >
        {Math.round(percent)}% time remaining
      </div>
    </div>
  );
}
export default MyComponent;