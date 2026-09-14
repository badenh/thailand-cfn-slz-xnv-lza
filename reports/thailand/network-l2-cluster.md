# L2 cluster: network domain hand-port shopping list

Items are [REWORK]-flagged from L1 — LZA models these at higher
abstraction than SLZ CFN. Reviewer must hand-port during task #9.

## `lz-account-vpc-template.yaml` (59 items)

- **12× AWS::EC2::SubnetRouteTableAssociation** → hand-port to LZA equivalent
- **9× AWS::EC2::RouteTable** → hand-port to LZA equivalent
- **9× AWS::EC2::Route** → hand-port to LZA equivalent
- **8× AWS::EC2::NetworkAclEntry** → hand-port to LZA equivalent
- **4× AWS::EC2::NetworkAcl** → hand-port to LZA equivalent
- **4× AWS::EC2::SubnetNetworkAclAssociation** → hand-port to LZA equivalent
- **4× AWS::EC2::EIP** → hand-port to LZA equivalent
- **4× AWS::EC2::NatGateway** → hand-port to LZA equivalent
- **1× AWS::EC2::DHCPOptions** → hand-port to LZA equivalent
- **1× AWS::EC2::VPCDHCPOptionsAssociation** → hand-port to LZA equivalent
- **1× AWS::EC2::InternetGateway** → hand-port to LZA equivalent
- **1× AWS::EC2::VPCGatewayAttachment** → hand-port to LZA equivalent
- **1× AWS::EC2::FlowLog** → hand-port to LZA equivalent

## `lz-central-network.json` (66 items)

- **15× AWS::EC2::RouteTable** → hand-port to LZA equivalent
- **15× AWS::EC2::SubnetRouteTableAssociation** → hand-port to LZA equivalent
- **12× AWS::EC2::Route** → hand-port to LZA equivalent
- **3× AWS::EC2::SubnetNetworkAclAssociation** → hand-port to LZA equivalent
- **3× AWS::EC2::EIP** → hand-port to LZA equivalent
- **3× AWS::EC2::NatGateway** → hand-port to LZA equivalent
- **2× AWS::EC2::NetworkAclEntry** → hand-port to LZA equivalent
- **2× AWS::EC2::FlowLog** → hand-port to LZA equivalent
- **2× AWS::EC2::TransitGatewayRouteTableAssociation** → hand-port to LZA equivalent
- **2× AWS::EC2::TransitGatewayRouteTablePropagation** → hand-port to LZA equivalent
- **2× AWS::EC2::TransitGatewayAttachment** → hand-port to LZA equivalent
- **1× AWS::EC2::InternetGateway** → hand-port to LZA equivalent
- **1× AWS::EC2::VPCGatewayAttachment** → hand-port to LZA equivalent
- **1× AWS::EC2::NetworkAcl** → hand-port to LZA equivalent
- **1× AWS::EC2::TransitGatewayRoute** → hand-port to LZA equivalent
- **1× AWS::EC2::SecurityGroup** → hand-port to LZA equivalent

## Hand-port guidance

**Routes + RouteTables + SubnetRouteTableAssociations:** collapse into `vpcs[].routeTables[].routes[]` per LZA schema.

**NetworkAcls + NetworkAclEntries + SubnetNetworkAclAssociations:** collapse into `vpcs[].networkAcls[]` with inline `inboundRules` / `outboundRules`.

**NatGateways + EIPs:** collapse into `vpcs[].natGateways[]` with `subnet:` and `allocationId:` fields.

**InternetGateway + VPCGatewayAttachment:** collapse into `vpcs[].internetGateway`.

**TGW attachments + route-table assoc + propagation + static routes:** collapse into `vpcs[].transitGatewayAttachments[]` on spoke VPCs and `transitGateways[].routeTables[].routes[]` on the central TGW.

**DHCPOptions + Association:** `vpcs[].dhcpOptions:` block.

**SecurityGroup:** `vpcs[].securityGroups[]`.

**FlowLog:** already folded into `vpcFlowLogs` global block; per-VPC entries can be dropped.
