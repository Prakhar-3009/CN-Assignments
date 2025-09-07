import dns.resolver
import logging

logging.basicConfig(filename="dns_query_results.txt",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def query_dns(domain):
    try:
        # 1. Resolve domain to IP address (A record)
        answers = dns.resolver.resolve(domain, 'A')
        logging.info(f"A records for {domain}:")
        for rdata in answers:
            logging.info(f"  {rdata.address}")
            print(f"A record: {rdata.address}")

        try:
            mx_answers = dns.resolver.resolve(domain, 'MX')
            logging.info(f"MX records for {domain}:")
            for rdata in mx_answers:
                logging.info(f"  Preference: {rdata.preference}, Mail Exchange: {rdata.exchange}")
                print(f"MX record: {rdata.exchange} (Preference: {rdata.preference})")
        except dns.resolver.NoAnswer:
            logging.info("No MX records found.")
            print("No MX records found.")

        try:
            cname_answers = dns.resolver.resolve(domain, 'CNAME')
            logging.info(f"CNAME records for {domain}:")
            for rdata in cname_answers:
                logging.info(f"  {rdata.target}")
                print(f"CNAME record: {rdata.target}")
        except dns.resolver.NoAnswer:
            logging.info("No CNAME records found.")
            print("No CNAME records found.")

    except dns.resolver.NXDOMAIN:
        logging.error(f"Domain {domain} does not exist.")
        print(f"Domain {domain} does not exist.")
    except Exception as e:
        logging.error(f"Error querying DNS for {domain}: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    domain_name = input("Enter the domain name to query: ")
    query_dns(domain_name)
    print("\nDNS query results have been logged to 'dns_query_results.txt'")
