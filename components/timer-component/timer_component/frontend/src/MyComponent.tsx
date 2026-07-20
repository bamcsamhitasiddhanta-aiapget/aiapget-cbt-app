import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { FC, ReactElement, useEffect, useState } from "react";

export type MyComponentStateShape = {
  expired: boolean;
};

export type MyComponentDataShape = {
  end_time: number;
};

export type MyComponentProps = Pick<
  FrontendRendererArgs<MyComponentStateShape, MyComponentDataShape>,
  "setStateValue"
> &
  MyComponentDataShape;

const MyComponent: FC<MyComponentProps> = ({
  end_time,
  setStateValue,
}): ReactElement => {
  const getRemaining = () =>
    Math.max(0, Math.floor(end_time - Date.now() / 1000));

  const [remaining, setRemaining] = useState(getRemaining());

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

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "80px",
        fontSize: "42px",
        fontWeight: "bold",
        fontFamily: "monospace",
      }}
    >
      {minutes}:{seconds}
    </div>
  );
};

export default MyComponent;