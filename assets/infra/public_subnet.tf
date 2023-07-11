# Create a public subnet
resource "aws_subnet" "tf_subnet" {
  vpc_id                  = aws_vpc.main.id
  availability_zone       = "${data.aws_region.all.names[0]}"
  cidr_block              = var.subnet_cidr
  map_public_ip_on_launch = true

  tags = {
    "Name" = "Public tfSubnet"
  }
}

resource "aws_subnet" "NATPublicSubnet" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet1_cidr
  availability_zone = "${data.aws_region.all.names[1]}"

  tags = {
    "Name" = "Public Subnet for NAT Gateway"
  }
}

# Create a public table
resource "aws_route_table" "tfRouteTable" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.tf_gateway.id
  }

  tags = {
    "Name" = "Public Subnet Route Table"
  }
}

resource "aws_route_table_association" "rt_associate_public" {
  subnet_id      = aws_subnet.tf_subnet.id
  route_table_id = aws_route_table.tfRouteTable.id
}