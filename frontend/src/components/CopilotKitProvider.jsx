import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export const CopilotKitProvider = ({ children }) => {
  return (
    <CopilotKit
      publicLicenseKey="ck_pub_a21c9b4bd5dbd3edd0c9e4edbded8100"
      runtimeUrl={`${BACKEND_URL}/api/copilotkit`}
      agent="codeforge_manager"
      showDevConsole={true}
    >
      {children}
    </CopilotKit>
  );
};

export default CopilotKitProvider;
