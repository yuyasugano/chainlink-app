pragma solidity ^0.6.0;

import "https://raw.githubusercontent.com/smartcontractkit/chainlink/develop/evm-contracts/src/v0.6/ChainlinkClient.sol";

contract TestConsumer is ChainlinkClient {
  
    uint256 public value;
    
    address private oracle;
    bytes32 private jobId;
    uint256 private fee;
    
    /**
     * Network: MainNet
     * Oracle: 0xb25FCb293571ba083bc33dA71159ed2a39A051A1
     * Job ID: 4144bfcb058245ecbbd746044d49762f
     * Fee: 0.1 LINK
     */
    constructor() public {
        setPublicChainlinkToken();
        oracle = 0xb25FCb293571ba083bc33dA71159ed2a39A051A1;
        jobId = "4144bfcb058245ecbbd746044d49762f";
        fee = 0.1 * 10 ** 18; // 0.1 LINK
    }

    /**
     * Create a Chainlink request to retrieve API response, find the target
     * data, then multiply by 1000000000000000000 (to remove decimal places from data).
     */
    function requestValue() public returns (bytes32 requestId) 
    {
        // initialize a request with a callback function
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);

        request.add("n", "bitcoin"); // add query parameter n(name) in data json
        request.add("p", "m");       // add query parameter p(period) in data json

        // Set the path to find the desired data in the API response:
        string[] memory path = new string[](2);
        path[0] = "disparity";
        path[1] = "5";
        request.addStringArray("copyPath", path);

        // Multiply the result by 1000000000000000000 to remove decimals
        int timesAmount = 10**18;
        request.addInt("times", timesAmount);
        return sendChainlinkRequestTo(oracle, request, fee);
    }

    /**
     * Receive the response in the form of uint256
     */ 
    function fulfill(bytes32 _requestId, uint256 _value) public recordChainlinkFulfillment(_requestId)
    {
        value = _value;
    }
}

