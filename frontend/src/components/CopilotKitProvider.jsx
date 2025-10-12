import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export const CopilotKitProvider = ({ children }) => {
  return (
    <CopilotKit
      runtimeUrl={`${BACKEND_URL}/api/copilotkit`}
      agent="codeforge_manager"
      showDevConsole={true}
    >
      {children}
    </CopilotKit>
  );
};

export default CopilotKitProvider;
