//
//  RootViewController.m
//  DBRoulette
//
//  Created by Brian Smith on 6/29/10.
//  Copyright Dropbox, Inc. 2010. All rights reserved.
//

#import "RootViewController.h"
#import <DropboxSDK/DropboxSDK.h>


@interface RootViewController ()

- (void)updateButtons;

@end

@implementation RootViewController {
    OTSession* _session;
    OTPublisher* _publisher;
    OTSubscriber* _subscriber;
    UIButton* _connectButton;
    UIButton* _disconnectButton;
    UIButton* _publishButton;
    UIButton* _unpublishButton;
    UIButton* _unsubscribeButton;
    UILabel* _statusLabel;
}


static int topOffset = 130;
static double widgetHeight = 400;
static double widgetWidth = 500;
static NSString* const kApiKey = @"14255491";
static NSString* const kToken = @"devtoken";
static NSString* const kSessionId = @"2_MX4xMjMyMDgxfjcyLjUuMTY3LjE0OH4yMDEyLTA0LTE1IDAwOjM1OjA1LjU0NTUwNyswMDowMH4wLjMxNjA0NjQ5NjQzNX4";
static bool subscribeToSelf = NO; // Change to NO if you want to subscribe streams other than your own



- (id)initWithCoder:(NSCoder *)aDecoder {
    if ((self = [super initWithCoder:aDecoder])) {
        self.title = @"Link Account";
    }
    return self;
}

- (void)didPressLink {
    if (![[DBSession sharedSession] isLinked]) {
		[[DBSession sharedSession] link];
    } else {
        [[DBSession sharedSession] unlinkAll];
        [[[[UIAlertView alloc] 
           initWithTitle:@"Account Unlinked!" message:@"Your dropbox account has been unlinked" 
           delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil]
          autorelease]
         show];
        [self updateButtons];
    }
}

- (DBRestClient *)restClient {
    if (!restClient) {
        restClient =
        [[DBRestClient alloc] initWithSession:[DBSession sharedSession]];
        restClient.delegate = self;
    }
    return restClient;
}


- (IBAction)didPresspic{

	// Create image picker controller
    UIImagePickerController *imagePicker = [[UIImagePickerController alloc] init];
    
    // Set source to the camera
	imagePicker.sourceType =  UIImagePickerControllerSourceTypeCamera;
    
    // Delegate is self
	imagePicker.delegate = self;
    
    // Allow editing of image ?
	imagePicker.allowsImageEditing = NO;
    
    // Show image picker
	[self presentModalViewController:imagePicker animated:YES];	
}


- (void) imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary *)info
{
    //NSError *error;
    
    // Access the uncropped image from info dictionary
    UIImage *image = [info objectForKey:@"UIImagePickerControllerOriginalImage"];
    
    // Create paths to output images
   //NSString  *pngPath = [NSHomeDirectory() stringByAppendingPathComponent:@"Documents/test.png"];
  NSString  *jpgPath = [NSHomeDirectory() stringByAppendingPathComponent:@"test.jpg"];
    
    // Write a UIImage to JPEG with minimum compression (best quality)
    // The value 'image' must be a UIImage object
    // The value '1.0' represents image compression quality as value from 0.0 to 1.0
    [UIImageJPEGRepresentation(image, 1.0) writeToFile:jpgPath atomically:YES];
    
    // Write image to PNG
   // [UIImagePNGRepresentation(image) writeToFile:pngPath atomically:YES];
    
    // Let's check to see if files were successfully written...
    // You can try this when debugging on-device
    
    // Create file manager
 //   NSFileManager *fileMgr = [NSFileManager defaultManager];
    
    // Point to Document directory
   // NSString *documentsDirectory = [NSHomeDirectory() stringByAppendingPathComponent:@""];
    
    
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *path = [[paths objectAtIndex:0] stringByAppendingString:@"test.jpg"];
    
    NSData * data = [NSData dataWithData:UIImageJPEGRepresentation(image, 1.0f)];
    [data writeToFile:path atomically:YES];
    NSString *MyString;
	NSDate *now = [NSDate date];
	NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
	[dateFormatter setDateFormat:@"HH-mm"];
	MyString = [dateFormatter stringFromDate:now];
	[dateFormatter release];

    NSString *filenamenew = [NSString stringWithFormat:@"%@-%@.jpg",[[UIDevice currentDevice] name], MyString];
    [self.restClient uploadFile:filenamenew toPath:@"/" withParentRev:nil fromPath:path];
/*
    // Write out the contents of home directory to console
    NSLog(@" directory: %@", [fileMgr contentsOfDirectoryAtPath:documentsDirectory error:&error]);
    NSString *localPath = [[NSBundle mainBundle] pathForResource:@"newpic" ofType:@"jpg"];
    NSString *filename = @"newpic.png";
    NSString *destDir = @"/";
    [[self restClient] uploadFile:filename toPath:destDir
                    withParentRev:nil fromPath:pngPath];
*/
    // Dismiss the camera
    [self dismissModalViewControllerAnimated:YES];
    
    [picker release];
}
- (void)restClient:(DBRestClient*)client uploadedFile:(NSString*)destPath
              from:(NSString*)srcPath metadata:(DBMetadata*)metadata {
    
    NSLog(@"File uploaded successfully to path: %@", metadata.path);
}

- (void)restClient:(DBRestClient*)client uploadFileFailedWithError:(NSError*)error {
    NSLog(@"File upload failed with error - %@", error);
}



- (IBAction)didPressPhotos {
    [self.navigationController pushViewController:photoViewController animated:YES];
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    [self updateButtons];
}

- (void)viewDidLoad {
    [super viewDidLoad];
    self.navigationItem.leftBarButtonItem = [[[UIBarButtonItem alloc] 
                                               initWithTitle:@"Take Photo" style:UIBarButtonItemStylePlain 
                                               target:self action:@selector(didPresspic)] autorelease];

    self.navigationItem.rightBarButtonItem = [[[UIBarButtonItem alloc] 
            initWithTitle:@"Photos" style:UIBarButtonItemStylePlain 
            target:self action:@selector(didPressPhotos)] autorelease];
    self.title = @"Project Wing";
    self.view.backgroundColor = [UIColor blackColor];
    [self createUI];
    [self doConnect];
}

- (void)createUI
{
    _connectButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    _connectButton.frame = CGRectMake(10, 10, 100, 44);
    [_connectButton setTitle:@"Connect" forState:UIControlStateNormal];
    [_connectButton addTarget:self
                       action:@selector(connectButtonClicked:)
             forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:_connectButton];    
    
    _disconnectButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    _disconnectButton.frame = CGRectMake(10, 10, 100, 44);
    [_disconnectButton setTitle:@"Disconnect" forState:UIControlStateNormal];
    [_disconnectButton addTarget:self
                          action:@selector(disconnectButtonClicked:)
                forControlEvents:UIControlEventTouchUpInside];
    _disconnectButton.hidden = YES;
    [self.view addSubview:_disconnectButton];    
    
    _publishButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    _publishButton.frame = CGRectMake(120, 10, 100, 44);
    [_publishButton setTitle:@"Publish" forState:UIControlStateNormal];
    [_publishButton addTarget:self
                       action:@selector(publishButtonClicked:)
             forControlEvents:UIControlEventTouchUpInside];
    _publishButton.hidden = YES;
    [self.view addSubview:_publishButton];    
    
    _unpublishButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    _unpublishButton.frame = CGRectMake(-120, -10, 100, 44);
    [_unpublishButton setTitle:@"Unpublish" forState:UIControlStateNormal];
    [_unpublishButton addTarget:self
                         action:@selector(unpublishButtonClicked:)
               forControlEvents:UIControlEventTouchUpInside];
    _unpublishButton.hidden = YES;
    [self.view addSubview:_unpublishButton];
    
    _unsubscribeButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    _unsubscribeButton.frame = CGRectMake(10, 10 + topOffset + widgetHeight * 2, 100, 44);
    [_unsubscribeButton setTitle:@"Unsubscribe" forState:UIControlStateNormal];
    [_unsubscribeButton addTarget:self
                           action:@selector(unsubscribeButtonClicked:)
                 forControlEvents:UIControlEventTouchUpInside];
    _unsubscribeButton.hidden = YES;
    [self.view addSubview:_unsubscribeButton];
    
    _statusLabel = [[UILabel alloc] init];
    //_statusLabel.frame = CGRectMake(230, 10, 240, 44);
    //[self setStatusLabel];
    //[self.view addSubview:_statusLabel];

}
- (void)connectButtonClicked:(UIButton*)button
{
    _connectButton.hidden = YES;
    [self doConnect];
}

- (void)disconnectButtonClicked:(UIButton*)button
{
    _disconnectButton.hidden = YES;
    [self doDisconnect];
}

- (void)publishButtonClicked:(UIButton*)button
{
    _publishButton.hidden = YES;
    [self doPublish];
}

- (void)unpublishButtonClicked:(UIButton*)button
{
    _unpublishButton.hidden = YES;
    [self doUnpublish];
}


- (void)unsubscribeButtonClicked:(UIButton*)button
{
    _unsubscribeButton.hidden = YES;
    [_subscriber close];
    _subscriber = nil;
}


- (void)viewDidUnload {
    [linkButton release];
    linkButton = nil;
}

- (void)dealloc {
    [linkButton release];
    [photoViewController release];
    [super dealloc];
}
- (void)updateSubscriber
{
    for (NSString* streamId in _session.streams) {
        OTStream* stream = [_session.streams valueForKey:streamId];
        if (stream.connection.connectionId != _session.connection.connectionId) {
            _subscriber = [[OTSubscriber alloc] initWithStream:stream delegate:self];
            break;
        }
    }
}


#pragma mark - OpenTok methods

- (void)doConnect 
{
    _session = [[OTSession alloc] initWithSessionId:kSessionId
                                           delegate:self];
    [_session addObserver:self
               forKeyPath:@"connectionCount"
                  options:NSKeyValueObservingOptionNew
                  context:nil];
    [_session connectWithApiKey:kApiKey token:kToken];
    _disconnectButton.hidden = YES;

}

- (void)doDisconnect 
{
    [_session disconnect];
}

- (void)doPublish
{
    _publisher = [[OTPublisher alloc] initWithDelegate:self name:UIDevice.currentDevice.name];
    _publisher.publishAudio = YES;
    _publisher.publishVideo = YES;
    [_session publish:_publisher];
    [self.view addSubview:_publisher.view];
    [_publisher.view setFrame:CGRectMake(0, topOffset, widgetWidth, widgetHeight)];
    
    _publishButton.hidden = YES;

    _disconnectButton.hidden = YES;
    _connectButton.hidden = YES;

    [_unpublishButton setHidden:YES];
    _unpublishButton.hidden = YES;

    
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context
{
    if ([keyPath isEqualToString:@"connectionCount"]) {
        [self setStatusLabel];
    }
}

- (void)doUnpublish
{
    [_session unpublish:_publisher];    
}

- (void)setStatusLabel
{
    if (_session && _session.connectionCount > 0) {
        _statusLabel.text = [NSString stringWithFormat:@"Connections: %d Streams: %d", _session.connectionCount, _session.streams.count];
    } else {
        _statusLabel.text = @"Not connected.";
    }
}

#pragma mark - OTSessionDelegate methods

- (void)sessionDidConnect:(OTSession*)session
{
    _disconnectButton.hidden = NO;
    _publishButton.hidden = NO;
    [self setStatusLabel];
    NSLog(@"sessionDidConnect: %@", session.sessionId);
    NSLog(@"- connectionId: %@", session.connection.connectionId);
    NSLog(@"- creationTime: %@", session.connection.creationTime);
}

- (void)sessionDidDisconnect:(OTSession*)session 
{
    _statusLabel.text = @"Disconnected from session.";
    _publishButton.hidden = YES;
    _unpublishButton.hidden = YES;
    NSLog(@"sessionDidDisconnect: %@", session.sessionId);    
    _connectButton.hidden = NO;
}

- (void)session:(OTSession*)session didFailWithError:(NSError*)error
{
    _connectButton.hidden = NO;
    NSLog(@"session:didFailWithError: %@", error.description);    
}

- (void)session:(OTSession*)mySession didReceiveStream:(OTStream*)stream
{
    [self setStatusLabel];
    NSLog(@"session: didReceiveStream:");
    NSLog(@"- connection.connectionId: %@", stream.connection.connectionId);
    NSLog(@"- connection.creationTime: %@", stream.connection.creationTime);
    NSLog(@"- session.sessionId: %@", stream.session.sessionId);
    NSLog(@"- streamId: %@", stream.streamId);
    NSLog(@"- type %@", stream.type);
    NSLog(@"- creationTime %@", stream.creationTime);
    NSLog(@"- name %@", stream.name);
    NSLog(@"- hasAudio %@", (stream.hasAudio ? @"YES" : @"NO"));
    NSLog(@"- hasVideo %@", (stream.hasVideo ? @"YES" : @"NO"));
    if ( (subscribeToSelf && [stream.connection.connectionId isEqualToString: _session.connection.connectionId])
        ||
        (!subscribeToSelf && ![stream.connection.connectionId isEqualToString: _session.connection.connectionId])
        ) {
        if (!_subscriber) {
            _subscriber = [[OTSubscriber alloc] initWithStream:stream delegate:self];
            _subscriber.subscribeToAudio = YES;
            _subscriber.subscribeToVideo = YES;
        }
        NSLog(@"subscriber.session.sessionId: %@", _subscriber.session.sessionId);
        NSLog(@"- stream.streamId: %@", _subscriber.stream.streamId);
        NSLog(@"- subscribeToAudio %@", (_subscriber.subscribeToAudio ? @"YES" : @"NO"));
        NSLog(@"- subscribeToVideo %@", (_subscriber.subscribeToVideo ? @"YES" : @"NO"));
    }
}

- (void)session:(OTSession*)session didDropStream:(OTStream*)stream
{
    [self setStatusLabel];
    NSLog(@"session didDropStream (%@)", stream.streamId);
    if (!subscribeToSelf
        && _subscriber
        && [_subscriber.stream.streamId isEqualToString: stream.streamId]) {
        _subscriber = nil;
        _unsubscribeButton.hidden = YES;
        [self updateSubscriber];
    }
}

#pragma mark - OTPublisherDelegate methods

- (void)publisher:(OTPublisher*)publisher didFailWithError:(NSError*) error {
    NSLog(@"publisher: %@ didFailWithError: %@", publisher, error.description);
}

- (void)publisherDidStartStreaming:(OTPublisher *)publisher
{
    _unpublishButton.hidden = NO;
    NSLog(@"publisherDidStartStreaming: %@", publisher);
    NSLog(@"- publisher.session: %@", publisher.session.sessionId);
    NSLog(@"- publisher.name: %@", publisher.name);
}

-(void)publisherDidStopStreaming:(OTPublisher*)publisher
{
    _publishButton.hidden = NO;
    NSLog(@"publisherDidStopStreaming:%@", publisher);
}

#pragma mark - OTSubscriberDelegate methods

- (void)subscriberDidConnectToStream:(OTSubscriber*)subscriber
{
    NSLog(@"subscriberDidConnectToStream (%@)", subscriber.stream.connection.connectionId);
    [subscriber.view setFrame:CGRectMake(widgetWidth, topOffset, widgetWidth, widgetHeight)];
    [self.view addSubview:subscriber.view];
}

- (void)subscriberVideoDataReceived:(OTSubscriber*)subscriber {
    NSLog(@"subscriberVideoDataReceived (%@)", subscriber.stream.streamId);
    _unsubscribeButton.hidden = NO;
}

- (void)subscriber:(OTSubscriber *)subscriber didFailWithError:(NSError *)error
{
    NSLog(@"subscriber: %@ didFailWithError: %@", subscriber.stream.streamId, error.description);
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)toInterfaceOrientation {
        return YES;
}


#pragma mark private methods

@synthesize linkButton;
@synthesize photoViewController;

- (void)updateButtons {
    NSString* title = [[DBSession sharedSession] isLinked] ? @"Unlink Dropbox" : @"Link Dropbox";
    [linkButton setTitle:title forState:UIControlStateNormal];
    [linkButton setHidden:YES];
    self.navigationItem.rightBarButtonItem.enabled = [[DBSession sharedSession] isLinked];
}

@end

