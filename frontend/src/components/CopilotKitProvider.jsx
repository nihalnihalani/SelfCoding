import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export const CopilotKitProvider = ({ children }) => {
  // Ensure HTTPS is used
  const runtimeUrl = `${BACKEND_URL}/api/copilotkit`;
  console.log("CopilotKit Runtime URL:", runtimeUrl);
  
  return (
    <CopilotKit
      runtimeUrl={runtimeUrl}
      showDevConsole={false}
    >
      {children}
    </CopilotKit>
  );
};

export default CopilotKitProvider;
