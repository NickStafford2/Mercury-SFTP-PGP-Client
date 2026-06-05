
she just needs us to send us a file every week that is secure. I wrote down waht she was saying. only picked up words. help me fix my notes: 


they need a pgp key


they have a tool called cleopatra. can generate keys. also send and recieve. 
moving forward now, they will move from passwords to php key and ssh key. 
pending approval from there side on security. once the ticket is approved, we can send them our keys. then they will whitelist our ip address. 



* They use Kleopatra as their tool for:

  * generating PGP key pairs
  * encrypting/decrypting files
  * sending and receiving encrypted data



# Original Notes

SFTP - Secure File Transfer Protocol
Molena?? 
Mercury
want a consolidated way to send information with customers. 
urgent and important items. 
file encryption?
they are talking about ip addresses. 
I am pretty sure they are talking about doc sharing
Based on what you've captured, I think the cleaned-up notes would look something like this:

**File Transfer / Security Setup**

* We need to set up a static IP for their whitelist. 
* They need our **PGP public key**.
* They use **Kleopatra** to generate PGP keys and to encrypt/decrypt files.

* The process will involve both:
	* A **PGP key** for file encryption.
	* An **SSH key** for SFTP authentication.
	
* They are moving away from password-based access and toward key-based authentication and encryption.
* Their security team has a ticket/request pending approval.

* Once approved:
	  1. We generate and provide our PGP public key and SSH public key.
	  2. They configure access on their side.
	  3. They whitelist our public IP address(es).
	  4. Secure file transfers can begin.

**Ongoing Process**

* We will send them a file on a weekly basis.
* Files will be transferred securely via SFTP.
* Files may also be encrypted using PGP before transfer for additional security.


# FIle Format
CSV file format
we get a file with all fields filled except two.


elegibility files. 

Melina Id Benefit name + demographic info, melena will send as part of normal order. 
Filename Format: Mercury_ALL_Eligibility_04302026
will be a placeholder for the information
WE will need to fill FulfillmentStatus and FulfillmentDate

Mercury_all_fulfilled_20260520.csv


data gets purged every week. 

We send them the fulfilled file every ??
We recieve it once per week.

Sean: can we add a column for ETA for backorders?



we need to change 
- filename field (just the date portion. the filename is the same as the name of the file that we are sending)
- FulfillmentStatus
- FulfillmentDate
